import type { ReactNode } from "react";
import "./globals.css";
import { DevBanner } from "../components/app/dev-banner";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <DevBanner />
        {children}
      </body>
    </html>
  );
}
