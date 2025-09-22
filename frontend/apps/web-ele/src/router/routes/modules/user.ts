import type { RouteRecordRaw } from 'vue-router';

import { $t } from '#/locales';

const routes: RouteRecordRaw[] = [
  {
    meta: {
      icon: 'ic:baseline-view-in-ar',
      keepAlive: true,
      order: 1000,
      title: $t('page.user.title'),
    },
    name: 'acl',
    path: '/acl',
    children: [
      {
        meta: {
          title: $t('page.user.userManagement'),
          authority: ['admin'],
        },
        name: 'user',
        path: '/acl/user',
        component: () => import('#/views/acl/user/index.vue'),
      },
      {
        meta: {
          title: $t('page.user.roleManagement'),
        },
        name: 'role',
        path: '/acl/role',
        component: () => import('#/views/acl/role/index.vue'),
      },
    ],
  },
];

export default routes;
