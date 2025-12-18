import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro/why-physical-ai-matters">
            Start Learning - 13 Week Journey 🚀
          </Link>
          <Link
            className="button button--primary button--lg"
            to="/docs/module-1/intro">
            Begin Module 1: The Robotic Nervous System ⚡
          </Link>
        </div>
      </div>
    </header>
  );
}

function HomepageHero() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <section className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className="row">
          <div className="col col--5 col--offset-1">
            <Heading as="h1" className="hero__title">
              {siteConfig.title}
            </Heading>
            <p className="hero__subtitle">
              {siteConfig.tagline}
            </p>
            <p>
              Welcome to the comprehensive e-book on Physical AI & Humanoid Robotics.
              This 13-week course teaches you how to build intelligent humanoid robots
              that excel in our human-centered world through advanced perception,
              cognition, and action systems.
            </p>
            <div className={styles.buttons}>
              <Link
                className="button button--secondary button--lg"
                to="/docs/intro/why-physical-ai-matters">
                Start Learning
              </Link>
              <Link
                className="button button--outline button--lg"
                to="/docs/weekly-breakdown/weeks-1-2">
                View Curriculum
              </Link>
            </div>
          </div>
          <div className="col col--5">
            <div className={styles.heroImage}>
              <img
                src="/img/hero-pic.png"
                alt="Humanoid Robot Illustration"
                style={{width: '100%', maxWidth: '400px', margin: '0 auto', display: 'block'}}
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function KeyBenefitsSection() {
  return (
    <section className="margin-top--lg">
      <div className="container padding-horiz--md">
        <div className="row">
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>Why Physical AI?</h3>
              <p>
                Unlike digital AI models confined to virtual environments, Physical AI systems operate in the continuous, noisy, and complex physical world.
                Humanoid robots excel in our human-centered world because they share our physical form and can be trained with abundant data from interacting in human environments.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>Complete Learning Path</h3>
              <p>
                13-week structured curriculum covering ROS 2, simulation, AI-brain systems,
                and vision-language-action integration. Each module builds upon the previous
                to create a comprehensive understanding of humanoid robotics.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>Hands-On Projects</h3>
              <p>
                Build complete robotic systems, implement perception algorithms,
                develop conversational AI interfaces, and create autonomous humanoid
                robots capable of understanding and executing natural language commands.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function CurriculumOverview() {
  return (
    <section className="margin-top--lg">
      <div className="container padding-horiz--md">
        <Heading as="h2" className={clsx('text--center', styles.sectionTitle)}>
          4-Module Learning Path
        </Heading>
        <div className="row margin-top--lg">
          <div className="col col--3">
            <div className="card">
              <div className="card__header">
                <h3>Module 1: The Robotic Nervous System</h3>
              </div>
              <div className="card__body">
                <p>ROS 2 fundamentals: nodes, topics, services, and bridging Python agents to ROS controllers</p>
              </div>
            </div>
          </div>
          <div className="col col--3">
            <div className="card">
              <div className="card__header">
                <h3>Module 2: The Digital Twin</h3>
              </div>
              <div className="card__body">
                <p>Gazebo & Unity: Physics simulation, gravity, collisions, and sensor simulation</p>
              </div>
            </div>
          </div>
          <div className="col col--3">
            <div className="card">
              <div className="card__header">
                <h3>Module 3: The AI-Robot Brain</h3>
              </div>
              <div className="card__body">
                <p>NVIDIA Isaac™: VSLAM, navigation, and path planning for bipedal humanoid movement</p>
              </div>
            </div>
          </div>
          <div className="col col--3">
            <div className="card">
              <div className="card__header">
                <h3>Module 4: Vision-Language-Action</h3>
              </div>
              <div className="card__body">
                <p>Voice-to-Action using OpenAI Whisper and cognitive planning with LLMs</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function CallToAction() {
  return (
    <section className="margin-top--lg margin-bottom--lg">
      <div className="container text--center padding-vert--xl">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <h2>Ready to Build the Future of Robotics?</h2>
            <p className="padding-horiz--md">
              Join thousands of learners mastering Physical AI & Humanoid Robotics.
              Start your journey today and become part of the next generation of
              roboticists building intelligent humanoid systems.
            </p>
            <Link
              className="button button--primary button--lg"
              to="/docs/intro/why-physical-ai-matters">
              Begin Your Learning Journey
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Learn Physical AI & Humanoid Robotics through a comprehensive 13-week e-book course">
      <HomepageHero />
      <main>
        <KeyBenefitsSection />
        <CurriculumOverview />
        <CallToAction />
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
