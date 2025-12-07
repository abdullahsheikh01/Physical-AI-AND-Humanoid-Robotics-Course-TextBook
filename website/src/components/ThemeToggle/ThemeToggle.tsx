import React from 'react';
import clsx from 'clsx';
import { useColorMode, useThemeConfig } from '@docusaurus/theme-common';
import styles from './ThemeToggle.module.css';

const ThemeToggle: React.FC = () => {
  const { colorMode, setColorMode } = useColorMode();
  const { navbar: { hideOnScroll } = {} } = useThemeConfig();

  const toggleColorMode = () => {
    setColorMode(colorMode === 'light' ? 'dark' : 'light');
  };

  // SVG Icons
  const SunIcon = () => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={styles.icon}
    >
      <circle cx="12" cy="12" r="5"></circle>
      <line x1="12" y1="1" x2="12" y2="3"></line>
      <line x1="12" y1="21" x2="12" y2="23"></line>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
      <line x1="1" y1="12" x2="3" y2="12"></line>
      <line x1="21" y1="12" x2="23" y2="12"></line>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
    </svg>
  );

  const MoonIcon = () => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={styles.icon}
    >
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
    </svg>
  );

  return (
    <button
      className={clsx(
        styles.themeToggle,
        'clean-btn',
        hideOnScroll && styles.themeToggleHideOnScroll
      )}
      onClick={toggleColorMode}
      aria-label={`Switch to ${colorMode === 'light' ? 'dark' : 'light'} mode`}
      title={`Switch to ${colorMode === 'light' ? 'dark' : 'light'} mode`}
    >
      <div className={styles.iconWrapper}>
        {colorMode === 'light' ? <MoonIcon /> : <SunIcon />}
      </div>
    </button>
  );
};

export default ThemeToggle;