import Catalog from "@/components/home/Catalog";
import Header from "@/components/home/Header";
import { HomeStateProvider } from "@/components/home/HomeState";
import {
  Advisor,
  Announce,
  Blog,
  CtaBand,
  Curriculum,
  Faq,
  Footer,
  Formats,
  Hero,
  Mentor,
  Outcomes,
  Paths,
  SkipLink,
  Stats,
  StickyBar,
  Strip,
  Why,
} from "@/components/home/Sections";

export default function HomePage() {
  return (
    <HomeStateProvider>
      <SkipLink />
      <Announce />
      <Header />
      <main id="main">
        <Hero />
        <Strip />
        <Catalog />
        <Stats />
        <Why />
        <Paths />
        <Curriculum />
        <Formats />
        <Outcomes />
        <Mentor />
        <Blog />
        <Advisor />
        <Faq />
        <CtaBand />
      </main>
      <Footer />
      <StickyBar />
    </HomeStateProvider>
  );
}
