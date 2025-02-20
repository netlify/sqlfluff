"""Implementation of Rule L033."""

from sqlfluff.core.rules.base import BaseRule, LintFix, LintResult


class Rule_L033(BaseRule):
    """UNION [DISTINCT|ALL] is preferred over just UNION.

    | **Anti-pattern**
    | In this example, UNION DISTINCT should be preferred over UNION, because
    | explicit is better than implicit.

    .. code-block:: sql

        SELECT a, b FROM table_1 UNION SELECT a, b FROM table_2

    | **Best practice**
    | Specify DISTINCT or ALL after UNION. (Note that DISTINCT is the default
    | behavior.

    .. code-block:: sql

        SELECT a, b FROM table_1 UNION DISTINCT SELECT a, b FROM table_2

    """

    def _eval(self, segment, raw_stack, **kwargs):
        """Look for UNION keyword not immediately followed by DISTINCT or ALL.

        Note that UNION DISTINCT is valid, rule only applies to bare UNION.
        The function does this by looking for a segment of type set_operator
        which has a UNION but no DISTINCT or ALL.
        """
        if segment.type == "set_operator":
            if "UNION" in segment.raw.upper() and not (
                "ALL" in segment.raw.upper() or "DISTINCT" in segment.raw.upper()
            ):
                union = self.make_keyword(
                    raw="UNION",
                    pos_marker=segment.pos_marker,
                )
                ins = self.make_whitespace(raw=" ", pos_marker=segment.pos_marker)
                distinct = self.make_keyword(
                    raw="DISTINCT",
                    pos_marker=segment.pos_marker,
                )
                return LintResult(
                    anchor=segment,
                    fixes=[
                        LintFix("edit", segment.segments[0], [union, ins, distinct])
                    ],
                )
        return LintResult()
