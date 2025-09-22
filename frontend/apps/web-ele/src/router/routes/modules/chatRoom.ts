import type { RouteRecordRaw } from 'vue-router';

import { $t } from '#/locales';

const routes: RouteRecordRaw[] = [
  {
    meta: {
      icon: 'lucide:layout-dashboard',
      order: -1,
      title: $t('page.chatRoom.title'),
    },
    name: 'chatRoom',
    path: '/chatRoom',
    component: () => import('#/views/chatRoom/index.vue'),

  },
];

export default routes;
