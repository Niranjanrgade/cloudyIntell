import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { WorkflowGraph } from "../../src/components/workflow/workflow-graph";

describe("WorkflowGraph", () => {
  it("renders active node state", () => {
    render(
      <WorkflowGraph
        events={[
          {
            event_id: "1",
            run_id: "run-1",
            provider: "aws",
            event_type: "state_transition",
            timestamp: new Date().toISOString(),
            node: { id: "aws-domain_generator", type: "domain_generator", state: "active" },
            payload: { status: "generating" },
          },
        ]}
      />,
    );

    expect(screen.getByText("Workflow Graph State")).toBeDefined();
    expect(screen.getByText(/Active node:/)).toBeDefined();
  });
});
