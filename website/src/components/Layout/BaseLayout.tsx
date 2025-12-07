import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import type { Props } from '@theme/Layout';
import styles from './BaseLayout.module.css';

const BaseLayout: React.FC<Props> = (props) => {
  const { children, ...layoutProps } = props;

  return (
    <Layout {...layoutProps}>
      <div className={clsx(styles.baseLayout)}>
        {children}
      </div>
    </Layout>
  );
};

export default BaseLayout;