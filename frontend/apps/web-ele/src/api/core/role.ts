import { requestClient } from '#/api/request';

export interface CreateRole {
  id?: number;
  role_name: string;
  role_status?: Boolean;
  role_desc?: string;
}

export interface RoleData {
  id?: number;
  role_name: string;
  role_status?: Boolean;
  role_desc?: string;
  create_time?: string;
  update_time?: string;
}

export interface RoleDataRes {
  items: RoleData[];
  total: number;
}

export interface MenuData {
  key: number;
  access_name: string;
  parent_id: number;
  scopes: string;
  access_desc: string;
  children?: MenuData[];
}

export interface MenuDataRes {
  all_access: MenuData[];
  role_access: number[];
}

export type MenuList = MenuData[];

export const reqAllRoleList = (page: number, limit: number, roleName: string) =>
  requestClient.get<RoleDataRes>('/role/list', {
    params: {
      size: limit,
      current: page,
      keyword: roleName,
    },
  });

export interface Role {
  value: number;
  label: string;
}
export type AllRole = Role[];

export interface UserRoleResp {
  all_role: AllRole;
  user_roles: number[];
}

export const reqAddOrUpdateRole = (data: RoleData) =>
  requestClient.post<RoleDataRes>('/role', data);

export const reqRemoveRole = (id: number) =>
  requestClient.delete<RoleDataRes>('/role', { params: { role_id: id } });

export const reqAllMenuList = (id: number) =>
  requestClient.get<MenuDataRes>('/access', { params: { role_id: id } });

export const reqSetPermission = (role_id: number, access: Number[]) =>
  requestClient.put('/access', { role_id, access });

export const reqUpdateUserRole = (id: number, data: number[]) =>
  requestClient.put('/user/set/role', { user_id: id, role_ids: data });

export const reqGetUserRole = (id: number) =>
  requestClient.get<UserRoleResp>('/role', { params: { user_id: id } });
