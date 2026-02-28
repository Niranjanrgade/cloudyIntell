import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { EvidenceSummary } from "../../src/components/evidence/evidence-summary";
import { RemediationPanel } from "../../src/components/evidence/remediation-panel";

const findings = [
  {
    finding_id: "f1",
    iteration: 0,
    domain: "compute" as const,
    outcome: "fail" as const,
    severity: "high" as const,
    reason: "Sizing issue",
    remediation: "Increase instance size",
    evidence: [{ source_uri: "u", title: "doc", availability_status: "available" as const }],
  },
];

describe("Evidence UI", () => {
  it("renders evidence and remediation", () => {
    render(
      <div>
        <EvidenceSummary findings={findings} />
        <RemediationPanel findings={findings} />
      </div>,
    );

    expect(screen.getByText("Evidence Summary")).toBeDefined();
    expect(screen.getByText("Remediation Guidance")).toBeDefined();
    expect(screen.getByText("Increase instance size")).toBeDefined();
  });
});
