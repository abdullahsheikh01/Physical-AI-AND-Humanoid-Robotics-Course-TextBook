import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useTaggedDocs, useTag } from '@docusaurus/theme-common/internal';
import type { Props } from '@theme/TagsListPage';
import type { Tag } from '@docusaurus/utils';

import styles from './tags.module.css';

function TagCard({ tag }: { tag: Tag }) {
  const taggedDocs = useTaggedDocs(tag);
  return (
    <div className="card margin-bottom--lg">
      <div className="card__header">
        <h3>
          <Link href={tag.permalink} className={styles.tagCardLink}>
            {tag.label} ({taggedDocs.length})
          </Link>
        </h3>
      </div>
      <div className="card__body">
        <ul className="padding--none">
          {taggedDocs.slice(0, 5).map((doc) => (
            <li key={doc.id} className="margin-bottom--sm">
              <Link href={doc.permalink}>{doc.metadata.title}</Link>
            </li>
          ))}
          {taggedDocs.length > 5 && (
            <li>
              <Link href={tag.permalink}>View all {taggedDocs.length} items...</Link>
            </li>
          )}
        </ul>
      </div>
    </div>
  );
}

export default function TagsList(): JSX.Element {
  const tags = useTag({
    allowHigherLevelTags: true,
  });

  return (
    <Layout title="Tags" description="Physical AI & Humanoid Robotics E-book Tags">
      <main className="container margin-vert--lg">
        <div className="row">
          <div className="col col--12">
            <h1>Tags</h1>
            <p>
              Browse content by tags to discover related topics in the Physical AI & Humanoid Robotics E-book.
            </p>

            <div className="margin-vert--lg">
              {tags.map((tag) => (
                <TagCard tag={tag} key={tag.permalink} />
              ))}
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}