import { requestClient } from '#/api/request';

export interface UserInfoResp {
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
}
export async function getUserInfoApi() {
  return requestClient.get<UserInfoResp>('/user/info');
}

export interface UserListItem {
  id: number;
  username: string;
  user_type: boolean;
  nickname?: string;
  user_phone?: string;
  user_email?: string;
  full_name?: string;
  user_status: boolean;
  avatar?: string;
  gender: number;
}
export interface UserListResp {
  total: number;
  items: UserListItem[];
}

export async function reqUserList(
  pageNo: number,
  pageSize: number,
  keyword: string,
) {
  return requestClient.get<UserListResp>('/user/list', {
    params: {
      size: pageSize,
      current: pageNo,
      keyword,
    },
  });
}

export interface User {
  id?: number;
  username: string;
  password: string;
}

export async function reqAddOrUpdateUser(data: User) {
  return requestClient.post('/user/add', data);
}

export async function reqRemoveUser(userId: number) {
  return requestClient.delete('/user/del', {
    params: {
      user_id: userId,
    },
  });
}
