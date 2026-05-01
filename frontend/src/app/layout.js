import "./globals.css";

export const metadata = {
  title: "MedSync — Healthcare Simulation Dashboard",
  description:
    "Real-time healthcare network simulation with Normal and Pandemic response modes. Monitor hospitals, patients, pharmacies, and infection curves.",
  keywords: "healthcare, simulation, hospital, pandemic, dashboard",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
