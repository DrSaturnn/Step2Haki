"""Structural extraction helpers for the standalone Board Brief page.

The page is deliberately kept as source HTML, so this module uses the Python
standard library's :class:`html.parser.HTMLParser` while retaining source
offsets and raw fragments. Callers that need to make a small surgical edit can
therefore use ``raw_start``/``raw_end`` instead of reserializing the document.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from html import unescape
from html.parser import HTMLParser
import re
from typing import Iterator, Optional


ARROW_RE = re.compile(r"(?:→|&rarr;|&#8594;|&#x2192;)", re.IGNORECASE)
_END_TAG_RE = re.compile(r"</\s*([A-Za-z][\w:-]*)\b[^>]*>", re.IGNORECASE)
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


@dataclass
class Node:
    """A source-backed HTML node."""

    tag: str
    source: str
    raw_start: int
    raw_end: int
    start_tag_end: int = 0
    end_tag_start: Optional[int] = None
    attrs: list[tuple[str, Optional[str]]] = field(default_factory=list)
    children: list["Node"] = field(default_factory=list)
    parent: Optional["Node"] = None
    raw_start_tag: str = ""
    self_closing: bool = False
    parse_error: Optional[str] = None

    @property
    def raw(self) -> str:
        return self.source[self.raw_start : self.raw_end]

    @property
    def raw_inner(self) -> str:
        end = self.end_tag_start if self.end_tag_start is not None else self.raw_end
        return self.source[self.start_tag_end : end]

    @property
    def attr_map(self) -> dict[str, Optional[str]]:
        out: dict[str, Optional[str]] = {}
        for name, value in self.attrs:
            out.setdefault(name, value)
        return out

    @property
    def class_tokens(self) -> set[str]:
        return set((self.attr_map.get("class") or "").split())

    def has_class(self, token: str) -> bool:
        return token in self.class_tokens

    def descendants(self, tag: Optional[str] = None) -> Iterator["Node"]:
        for child in self.children:
            if child.tag not in {"#text", "#comment"} and (
                tag is None or child.tag == tag.lower()
            ):
                yield child
            yield from child.descendants(tag)

    @property
    def text_content(self) -> str:
        return _normalize_space("".join(_decode_text_node(c) for c in self.children))


def _normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _decode_text_node(node: Node) -> str:
    if node.tag == "#text":
        # HTMLParser is configured with convert_charrefs=False, so this is the
        # sole entity decode performed by the accessor.
        return unescape(node.raw)
    if node.tag == "#comment":
        return ""
    return "".join(_decode_text_node(c) for c in node.children)


class _SourceParser(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.root = Node("#document", source, 0, len(source))
        self.stack: list[Node] = [self.root]
        self.cursor = 0
        self.errors: list[str] = []

    def _locate(self, raw: str) -> tuple[int, int]:
        if not raw:
            return self.cursor, self.cursor
        start = self.source.find(raw, self.cursor)
        if start < 0:
            start = self.cursor
            self.errors.append(f"source fragment not found at offset {self.cursor}")
        end = min(len(self.source), start + len(raw))
        self.cursor = end
        return start, end

    def _append(self, node: Node) -> None:
        node.parent = self.stack[-1]
        self.stack[-1].children.append(node)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        raw_tag = self.get_starttag_text() or ""
        start, end = self._locate(raw_tag)
        if tag.lower() == "li":
            # HTML's list-item insertion mode implicitly closes an open li
            # before starting the next sibling. HTMLParser does not implement
            # that browser rule, so do it here and retain an error locator.
            open_li = next((i for i in range(len(self.stack) - 1, 0, -1) if self.stack[i].tag == "li"), None)
            if open_li is not None:
                for node in self.stack[open_li:]:
                    node.parse_error = node.parse_error or f"implicitly closed before <li> at {start}"
                    node.raw_end = start
                    node.end_tag_start = None
                self.stack = self.stack[:open_li]
        node = Node(
            tag.lower(), self.source, start, end, start_tag_end=end,
            attrs=list(attrs), raw_start_tag=raw_tag,
        )
        self._append(node)
        if tag.lower() not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, Optional[str]]]
    ) -> None:
        raw_tag = self.get_starttag_text() or ""
        start, end = self._locate(raw_tag)
        self._append(Node(
            tag.lower(), self.source, start, end, start_tag_end=end,
            end_tag_start=end, attrs=list(attrs), raw_start_tag=raw_tag,
            self_closing=True,
        ))

    def handle_endtag(self, tag: str) -> None:
        match = _END_TAG_RE.search(self.source, self.cursor)
        if match is None:
            self.errors.append(f"end tag </{tag}> has no source locator at {self.cursor}")
            return
        start, end = match.span()
        self.cursor = end
        wanted = tag.lower()
        found = None
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == wanted:
                found = index
                break
        if found is None:
            self.errors.append(f"unmatched end tag </{tag}> at {start}")
            return
        if found != len(self.stack) - 1:
            self.errors.append(f"misnested end tag </{tag}> at {start}")
            for node in self.stack[found + 1 :]:
                node.parse_error = f"implicitly closed before </{tag}> at {start}"
                node.raw_end = start
                node.end_tag_start = start
            self.stack = self.stack[: found + 1]
        node = self.stack.pop()
        node.end_tag_start = start
        node.raw_end = end

    def handle_data(self, data: str) -> None:
        if not data:
            return
        start, end = self._locate(data)
        self._append(Node("#text", self.source, start, end, start_tag_end=start))

    def handle_entityref(self, name: str) -> None:
        raw = f"&{name};"
        start, end = self._locate(raw)
        self._append(Node("#text", self.source, start, end, start_tag_end=start))

    def handle_charref(self, name: str) -> None:
        raw = f"&#{name};"
        start, end = self._locate(raw)
        self._append(Node("#text", self.source, start, end, start_tag_end=start))

    def handle_comment(self, data: str) -> None:
        raw = f"<!--{data}-->"
        start, end = self._locate(raw)
        self._append(Node("#comment", self.source, start, end, start_tag_end=end))

    def handle_decl(self, decl: str) -> None:
        raw = f"<!{decl}>"
        start, end = self._locate(raw)
        self._append(Node("#decl", self.source, start, end, start_tag_end=end))

    def unknown_decl(self, data: str) -> None:
        raw = f"<![{data}]>"
        start, end = self._locate(raw)
        self._append(Node("#decl", self.source, start, end, start_tag_end=end))

    def handle_pi(self, data: str) -> None:
        raw = f"<?{data}>"
        start, end = self._locate(raw)
        self._append(Node("#pi", self.source, start, end, start_tag_end=end))

    def finish(self) -> None:
        if len(self.stack) > 1:
            for node in self.stack[1:]:
                node.raw_end = max(node.raw_end, node.start_tag_end, len(self.source))
                node.end_tag_start = None
                node.parse_error = node.parse_error or "unclosed element"
                self.errors.append(f"unclosed <{node.tag}> at {node.raw_start}")
            self.stack = [self.root]
        self.root.raw_end = len(self.source)


def parse_html(source: str) -> "Document":
    parser = _SourceParser(source)
    try:
        parser.feed(source)
        parser.close()
    except Exception as exc:  # pragma: no cover - defensive locator reporting
        parser.errors.append(f"HTML parser error at {parser.cursor}: {exc}")
    parser.finish()
    return Document(source, parser.root, parser.errors)


@dataclass
class ItemRecord:
    brief_id: str
    index: int
    bank_index: int
    node: Node
    attrs: list[tuple[str, Optional[str]]]
    segments: list[str]
    segment_html: list[str]
    stem: str
    answer: str
    companion: str
    parse_error: Optional[str] = None

    @property
    def raw_start(self) -> int:
        return self.node.raw_start

    @property
    def raw_end(self) -> int:
        return self.node.raw_end

    @property
    def raw_html(self) -> str:
        return self.node.raw

    @property
    def attr_map(self) -> dict[str, Optional[str]]:
        return self.node.attr_map

    @property
    def source_attributes(self) -> list[tuple[str, Optional[str]]]:
        return list(self.attrs)

    @property
    def locator(self) -> dict[str, int | str]:
        return {"brief_id": self.brief_id, "bank_index": self.bank_index}


@dataclass
class NoteRecord:
    brief_id: str
    index: int
    node: Node

    @property
    def raw_start(self) -> int:
        return self.node.raw_start

    @property
    def raw_end(self) -> int:
        return self.node.raw_end

    @property
    def raw_html(self) -> str:
        return self.node.raw

    @property
    def text(self) -> str:
        return self.node.text_content


@dataclass
class BriefRecord:
    node: Node
    id: str
    is_board_style: bool
    items: list[ItemRecord]
    notes: list[NoteRecord]

    @property
    def raw_start(self) -> int:
        return self.node.raw_start

    @property
    def raw_end(self) -> int:
        return self.node.raw_end

    @property
    def raw_html(self) -> str:
        return self.node.raw

    @property
    def inner_html(self) -> str:
        return self.node.raw_inner

    @property
    def attrs(self) -> list[tuple[str, Optional[str]]]:
        return list(self.node.attrs)

    @property
    def attr_map(self) -> dict[str, Optional[str]]:
        return self.node.attr_map

    @property
    def source_attributes(self) -> list[tuple[str, Optional[str]]]:
        return self.attrs

    @property
    def title(self) -> str:
        for node in self.node.descendants():
            if node.tag in {"h1", "h2", "h3", "h4", "h5"}:
                return node.text_content
        return ""

    @property
    def text(self) -> str:
        return self.node.text_content

    def blocks(self, cls: str) -> list[Node]:
        return [node for node in self.node.descendants() if node.has_class(cls)]


class Document:
    def __init__(self, source: str, root: Node, errors: list[str]):
        self.source = source
        self.root = root
        self.errors = list(errors)
        self.brief_records = self._collect_briefs()

    def _collect_briefs(self) -> list[BriefRecord]:
        records: list[BriefRecord] = []
        for node in self.root.descendants():
            if not node.has_class("brief"):
                continue
            bid = node.attr_map.get("id") or ""
            items: list[ItemRecord] = []
            notes: list[NoteRecord] = []
            typed_index = 0
            bank_index = 0
            for bank in node.descendants("ol"):
                if not bank.has_class("bank"):
                    continue
                for child in bank.children:
                    if child.tag != "li":
                        continue
                    bank_index += 1
                    attrs = child.attr_map
                    if attrs.get("data-type") is None:
                        notes.append(NoteRecord(bid, len(notes) + 1, child))
                        continue
                    typed_index += 1
                    items.append(_item_from_node(bid, typed_index, bank_index, child))
            records.append(BriefRecord(node, bid, node.has_class("bs"), items, notes))
        return records

    @property
    def briefs(self) -> list[BriefRecord]:
        return list(self.brief_records)

    @property
    def items(self) -> list[ItemRecord]:
        return [item for brief in self.brief_records for item in brief.items]

    @property
    def notes(self) -> list[NoteRecord]:
        return [note for brief in self.brief_records for note in brief.notes]

    def find_brief(self, brief_id: str) -> Optional[BriefRecord]:
        return next((brief for brief in self.brief_records if brief.id == brief_id), None)


def _split_top_level_segments(li: Node) -> tuple[list[str], list[str]]:
    """Return raw and normalized segments split by direct-child arrows only."""
    raw_segments: list[str] = [""]
    for child in li.children:
        raw = child.raw
        if child.tag == "#text":
            pieces = ARROW_RE.split(raw)
            arrows = ARROW_RE.findall(raw)
            raw_segments[-1] += pieces[0]
            for piece in pieces[1:]:
                raw_segments.append(piece)
        else:
            # An arrow inside <b>, <span>, or any other inline element is
            # content and therefore remains in the current segment.
            raw_segments[-1] += raw
    return raw_segments, [_normalize_space(text(fragment)) for fragment in raw_segments]


def _item_from_node(brief_id: str, index: int, bank_index: int, node: Node) -> ItemRecord:
    raw_segments, segments = _split_top_level_segments(node)
    error = None
    if len(segments) < 2:
        error = f"ambiguous item at {node.raw_start}: expected a top-level arrow"
    stem = segments[0] if segments else ""
    answer = segments[1] if len(segments) > 1 else ""
    companion = " → ".join(segments[2:]) if len(segments) > 2 else ""
    return ItemRecord(
        brief_id, index, bank_index, node, list(node.attrs), segments,
        raw_segments, stem, answer, companion, error,
    )


def _fragment_document(fragment: str) -> Document:
    return parse_html(fragment)


def text(value: str | None) -> str:
    """Normalize visible text while decoding character references exactly once."""
    if not value:
        return ""
    return _fragment_document(value).root.text_content


def blocks(body: str, cls: str) -> list[str]:
    """Return all class-token-matched block inner fragments in ``body``."""
    doc = _fragment_document(body)
    return [node.raw_inner for node in doc.root.descendants() if node.has_class(cls)]


def block(body: str, cls: str) -> Optional[str]:
    """Compatibility helper returning the first class-token-matched block."""
    found = blocks(body, cls)
    return found[0] if found else None


def briefs(source: str) -> Iterator[tuple[bool, str, str]]:
    """Compatibility helper yielding ``(is_board_style, id, inner_html)``."""
    for brief in parse_html(source).briefs:
        yield brief.is_board_style, brief.id, brief.inner_html


def iter_items(source: str) -> Iterator[ItemRecord]:
    yield from parse_html(source).items
