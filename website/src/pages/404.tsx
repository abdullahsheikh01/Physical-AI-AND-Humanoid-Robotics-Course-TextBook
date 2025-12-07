import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './404.module.css';

function NotFound() {
  return (
    <Layout title="Page Not Found" description="The requested page does not exist">
      <main className="container margin-vert--xl">
        <div className={styles.hero}>
          <div className={styles.heroContent}>
            <Heading as="h1" className={styles.heroTitle}>
              Page Not Found
            </Heading>
            <p className={styles.heroSubtitle}>
              We couldn't find the page you were looking for.
            </p>
            <div className={styles.indexCtas}>
              <Link className="button button--primary button--lg margin-right--sm" to="/">
                Back to Home
              </Link>
              <Link className="button button--secondary button--lg" to="/docs/intro">
                Explore E-book
              </Link>
            </div>
            <div className={styles.sitemapLinks}>
              <h3>Popular Sections:</h3>
              <ul>
                <li><Link to="/docs/intro">Introduction to Physical AI</Link></li>
                <li><Link to="/docs/module-1">Module 1: The Robotic Nervous System (ROS 2)</Link></li>
                <li><Link to="/docs/module-2">Module 2: The Digital Twin (Gazebo & Unity)</Link></li>
                <li><Link to="/docs/module-3">Module 3: The AI-Robot Brain (NVIDIA Isaac™)</Link></li>
                <li><Link to="/docs/module-4">Module 4: Vision-Language-Action (VLA)</Link></li>
                <li><Link to="/docs/weekly-breakdown">Weekly Breakdown</Link></li>
                <li><Link to="/docs/assessments">Assessments</Link></li>
                <li><Link to="/blog">Course Benefits Blog</Link></li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

export default NotFound;