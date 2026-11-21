import { HomeStateProvider } from "@/components/shared/HomeState";
import Motion from "@/components/shared/Motion";
import Header from "@/components/sections/Header";
import Hero from "@/components/sections/Hero";
import Employers from "@/components/sections/Employers";
import Ticker from "@/components/sections/Ticker";
import Courses from "@/components/sections/Courses";
import Stats from "@/components/sections/Stats";
import Features from "@/components/sections/Features";
import CareerPaths from "@/components/sections/CareerPaths";
import Curriculum from "@/components/sections/Curriculum";
import Formats from "@/components/sections/Formats";
import Testimonials from "@/components/sections/Testimonials";
import Mentor from "@/components/sections/Mentor";
import LearningHub from "@/components/sections/LearningHub";
import CounsellingForm from "@/components/sections/CounsellingForm";
import FAQ from "@/components/sections/FAQ";
import ClosingCTA from "@/components/sections/ClosingCTA";
import Footer from "@/components/sections/Footer";

export default function HomePage() {
  return (
    <HomeStateProvider>
      <Motion />
      <Header />
      <main id="main">
        <Hero />
        <Employers />
        <Ticker />
        <Courses />
        <Stats />
        <Features />
        <CareerPaths />
        <Curriculum />
        <Formats />
        <Testimonials />
        <Mentor />
        <LearningHub />
        <CounsellingForm />
        <FAQ />
        <ClosingCTA />
      </main>
      <Footer />
    </HomeStateProvider>
  );
}
