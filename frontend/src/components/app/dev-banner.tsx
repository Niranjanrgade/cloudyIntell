export function DevBanner() {
  const mode = process.env.NEXT_PUBLIC_CLOUDYINTEL_MODE ?? "local";
  if (mode !== "local") {
    return null;
  }

  return (
    <div className="bg-amber-100 px-4 py-2 text-xs font-medium text-amber-900">
      Authentication is disabled. Local/development mode only.
    </div>
  );
}
