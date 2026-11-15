"use client";

import { flushSync } from "react-dom";
import { filterKeys } from "@/content/site";
import { scrollToId, useHomeState } from "./HomeState";

type AnchorProps = React.AnchorHTMLAttributes<HTMLAnchorElement>;

/** Link that applies a catalog filter (or keyword search) before navigating. */
export function JumpLink({ jump, href, onClick, ...rest }: AnchorProps & { jump: string; href: string }) {
  const { setFilter, setQuery } = useHomeState();
  return (
    <a
      href={href}
      {...rest}
      onClick={(e) => {
        flushSync(() => {
          if (filterKeys.includes(jump)) {
            setFilter(jump);
            setQuery("");
          } else {
            setFilter("all");
            setQuery(jump);
          }
        });
        if (jump === "recorded" || jump === "live") {
          e.preventDefault();
          scrollToId(jump);
        }
        onClick?.(e);
      }}
    />
  );
}

/** Link to a course card: clears filters first so the target card is visible. */
export function ResetLink({ onClick, ...rest }: AnchorProps) {
  const { reset } = useHomeState();
  return (
    <a
      {...rest}
      onClick={(e) => {
        flushSync(reset);
        onClick?.(e);
      }}
    />
  );
}

/** "Ask an advisor": pre-fills the counselling form, then follows the anchor. */
export function AdvisorLink({ course, format, ...rest }: AnchorProps & { course: string; format: string }) {
  const { prefillForm } = useHomeState();
  return <a {...rest} onClick={() => prefillForm(course, format)} />;
}
