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
