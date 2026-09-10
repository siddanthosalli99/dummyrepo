import "./globals.css";

export const metadata = {
  title: "DummyPro",
  description: "Insurance Charges Prediction",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}