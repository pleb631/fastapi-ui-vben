import { acceptHMRUpdate, defineStore } from 'pinia';

interface BasicUserInfo {
  id: number;
  username: string;
  age?: number;
  user_type: boolean;
  nickname?: string;
  user_phone?: string;
  user_emai?: string;
  full_name?: string;
  user_status: boolean;
  avatar?: string;
  gender: number;
  roles?: string[];
}

interface AccessState {

  userInfo: BasicUserInfo | null;

  userRoles: string[];
}

/**
 * @zh_CN 用户信息相关
 */
export const useUserStore = defineStore('core-user', {
  actions: {
    setUserInfo(userInfo: BasicUserInfo | null) {
      this.userInfo = userInfo;
      if (userInfo?.roles){
        this.setUserRoles(userInfo.roles);
      }
    },
    setUserRoles(roles: string[]) {
      this.userRoles = roles;
    },
  },
  state: (): AccessState => ({
    userInfo: null,
    userRoles: [],
  }),
});

// 解决热更新问题
const hot = import.meta.hot;
if (hot) {
  hot.accept(acceptHMRUpdate(useUserStore, hot));
}
