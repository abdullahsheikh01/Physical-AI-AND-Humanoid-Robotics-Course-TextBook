import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import { useLocation } from '@docusaurus/router';
import styles from './RoboticFooter.module.css';

interface FooterLink {
  label: string;
  to: string;
}

interface FooterColumn {
  title: string;
  links: FooterLink[];
}

const RoboticFooter: React.FC = () => {
  const location = useLocation();

  // Define footer columns
  const footerColumns: FooterColumn[] = [
    {
      title: 'Modules',
      links: [
        { label: 'Module 1: The Robotic Nervous System (ROS 2)', to: '/docs/module-1' },
        { label: 'Module 2: The Digital Twin (Gazebo & Unity)', to: '/docs/module-2' },
        { label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)', to: '/docs/module-3' },
        { label: 'Module 4: Vision-Language-Action (VLA)', to: '/docs/module-4' },
      ],
    },
    {
      title: 'Resources',
      links: [
        { label: 'Weekly Breakdown', to: '/docs/weekly-breakdown' },
        { label: 'Assessments', to: '/docs/assessments' },
        { label: 'Blog', to: '/blog' },
      ],
    },
    {
      title: 'More',
      links: [
        { label: 'GitHub', to: 'https://github.com/your-org/physical-ai-humanoid-robotics-ebook' },
      ],
    },
  ];

  return (
    <footer className={clsx(styles.footer, 'footer')}>
      <div className="container">
        <div className="row">
          {footerColumns.map((column, index) => (
            <div key={index} className="col col--4">
              <h3 className={styles.footerTitle}>{column.title}</h3>
              <ul className={styles.footerLinks}>
                {column.links.map((link, linkIndex) => (
                  <li key={linkIndex}>
                    <Link
                      to={link.to}
                      className={clsx(styles.footerLink, {
                        [styles.active]: location.pathname === link.to
                      })}
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className={styles.copyright}>
          <p>Copyright © {new Date().getFullYear()} Physical AI & Humanoid Robotics E-book. Built with Docusaurus.</p>
        </div>
      </div>
    </footer>
  );
};

export default RoboticFooter;