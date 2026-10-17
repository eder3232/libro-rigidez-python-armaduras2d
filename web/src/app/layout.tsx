import type { Metadata } from "next";
import localFont from "next/font/local";
import Link from "next/link";
import "katex/dist/katex.min.css";
import "./globals.css";

// Las mismas familias tipográficas del PDF (licencia SIL OFL, ver src/fuentes/).
const serif = localFont({
  variable: "--fuente-serif",
  src: [
    { path: "../fuentes/LibertinusSerif-Regular.otf", weight: "400", style: "normal" },
    { path: "../fuentes/LibertinusSerif-Italic.otf", weight: "400", style: "italic" },
    { path: "../fuentes/LibertinusSerif-Bold.otf", weight: "700", style: "normal" },
    { path: "../fuentes/LibertinusSerif-BoldItalic.otf", weight: "700", style: "italic" },
  ],
});

const sans = localFont({
  variable: "--fuente-sans",
  src: [
    { path: "../fuentes/LibertinusSans-Regular.otf", weight: "400", style: "normal" },
    { path: "../fuentes/LibertinusSans-Bold.otf", weight: "700", style: "normal" },
  ],
});

const mono = localFont({
  variable: "--fuente-mono",
  src: [
    { path: "../fuentes/SourceCodePro-Regular.otf", weight: "400", style: "normal" },
    { path: "../fuentes/SourceCodePro-Bold.otf", weight: "700", style: "normal" },
  ],
});

export const metadata: Metadata = {
  title: {
    default: "Análisis matricial de armaduras con Python",
    template: "%s · Análisis matricial de armaduras con Python",
  },
  description: "Aprende el método de rigidez construyendo tu propia calculadora.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="es" className={`${serif.variable} ${sans.variable} ${mono.variable}`}>
      <body>
        <header className="cabecera">
          <Link href="/">Análisis matricial de armaduras con Python</Link>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
