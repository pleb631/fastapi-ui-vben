<template>
  <div>
    <el-card style="margin: 10px 0">
      <el-button type="primary" size="default" icon="Plus" @click="addRole">
        添加职位
      </el-button>
      <el-table border style="margin: 10px 0" :data="allRole">
        <el-table-column
          type="index"
          align="center"
          label="#"
        ></el-table-column>
        <el-table-column
          label="职位名称"
          align="center"
          show-overflow-tooltip
          prop="role_name"
        ></el-table-column>
        <el-table-column
          label="创建时间"
          align="center"
          show-overflow-tooltip
          prop="create_time"
        ></el-table-column>
        <el-table-column
          label="更新时间"
          align="center"
          show-overflow-tooltip
          prop="update_time"
        ></el-table-column>
        <el-table-column label="操作" width="280px" align="center">
          <template #="{ row }">
            <el-button size="small" @click="setPermission(row)">
              分配权限
            </el-button>
            <el-button type="primary" size="small"> 编辑 </el-button>
            <el-popconfirm
              :title="`你确定要删除${row.role_name}?`"
              width="260px"
              @confirm="removeRole(row.id)"
            >
              <template #reference>
                <el-button type="danger" size="small"> 删除 </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-model:current-page="pageNo"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 30, 40]"
        :background="true"
        layout="prev, pager, next, jumper , ->, sizes, total, "
        :total="total"
        @current-change="getHasRole"
        @size-change="sizeHandler"
      />
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="RoleParams.id ? '更新职位' : '添加职位'"
    >
      <el-form :model="RoleParams" :rules="rules" ref="formRef">
        <el-form-item label="职位名称" prop="role_name">
          <el-input
            placeholder="请你输入职位名称"
            v-model="RoleParams.role_name"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button size="default" @click="dialogVisible = false"
          >取消</el-button
        >
        <el-button type="primary" size="default" @click="save">确定</el-button>
      </template>
    </el-dialog>
    <el-drawer v-model="drawer">
      <template #header>
        <h4>分配菜单与按钮的权限</h4>
      </template>
      <template #default>
        <el-tree
          ref="tree"
          :data="menuArr"
          show-checkbox
          node-key="key"
          default-expand-all
          :default-checked-keys="selectArr"
          :props="defaultProps"
        />
      </template>
      <template #footer>
        <div style="flex: auto">
          <el-button @click="drawer = false">取消</el-button>
          <el-button type="primary" @click="handler">确定</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>
<script lang="ts" setup>
import { ref, onMounted, nextTick } from 'vue';
import {
  ElCard,
  ElButton,
  ElTable,
  ElTableColumn,
  ElPagination,
  ElMessage,
  ElForm,
  ElFormItem,
  ElInput,
  ElDialog,
  ElPopconfirm,
  ElTree,
  ElDrawer,
} from 'element-plus';

import type {
  RoleData,
  RoleDataRes,
  CreateRole,
  MenuList,
  MenuDataRes,
  MenuData
} from '#/api';
import {
  reqAllRoleList,
  reqAddOrUpdateRole,
  reqRemoveRole,
  reqAllMenuList,
  reqSetPermission,
} from '#/api';

let pageNo = ref<number>(1);

let pageSize = ref<number>(10);

onMounted(() => {
  getHasRole();
});

let keyword = ref<string>('');

let allRole = ref<RoleData[]>([]);

let total = ref<number>(0);

const getHasRole = async (pager = 1) => {
  pageNo.value = pager;
  let res: RoleDataRes = await reqAllRoleList(
    pageNo.value,
    pageSize.value,
    keyword.value,
  );
  if (res) {
    total.value = res.total;
    allRole.value = res.items;
  }
};

const sizeHandler = () => {
  getHasRole();
};

const dialogVisible = ref<boolean>(false);
const formRef = ref<any>(null);
const addRole = () => {
  dialogVisible.value = true;
  Object.assign(RoleParams, {
    roleName: '',
    id: 0,
  });
  nextTick(() => {
    formRef.value.clearValidate('role_name');
  });
};

const RoleParams = ref<CreateRole>({
  role_name: '',
});

const validateRoleName = (rule: any, value: any, callBack: any) => {
  if (value.trim().length >= 2) {
    callBack();
  } else {
    callBack(new Error('职位名称至少两位'));
  }
};

const rules = {
  role_name: [{ required: true, trigger: 'blur', validator: validateRoleName }],
};

const save = async () => {
  await formRef.value.validate();
  let res: any = await reqAddOrUpdateRole(RoleParams.value);
  if (res) {
    ElMessage({
      type: 'success',
      message: RoleParams.value.id ? '更新成功' : '添加成功',
    });
    dialogVisible.value = false;
    getHasRole(RoleParams.value.id ? pageNo.value : 1);
  }
};

const removeRole = async (id: number) => {
  let res: any = await reqRemoveRole(id);
  if (res) {
    ElMessage({
      type: 'success',
      message: '删除成功',
    });
    getHasRole(allRole.value.length > 1 ? pageNo.value : pageNo.value - 1);
  }
};

const drawer = ref(false);
const menuArr = ref<MenuList>([]);
const selectArr = ref<number[]>([]);

const defaultProps = {
  children: 'children',
  label: 'access_name',
};
const tree = ref();

const handler = async () => {
  const roleId = RoleParams.id as number;
  let arr = tree.value.getCheckedKeys();
  let arr1 = tree.value.getHalfCheckedKeys();
  let permissionId = arr.concat(arr1);
  let res: any = await reqSetPermission(roleId, permissionId);
  if (res) {
      drawer.value = false;
      ElMessage({
          type: "success",
          message: "分配权限成功",
      });
  }
};
function findLeafKeys(menuList: MenuData[], keys: number[]): number[] {
  const result: number[] = [];

  const dfs = (nodes: MenuData[]) => {
    for (const node of nodes) {
      const hasChildren = node.children && node.children.length > 0;

      if (keys.includes(node.key) && !hasChildren) {
        result.push(node.key);
      }

      if (hasChildren) {
        dfs(node.children!);
      }
    }
  };

  dfs(menuList);
  return result;
}
const setPermission = async (row: RoleData) => {
  drawer.value = true;
  Object.assign(RoleParams, row);
  let res: MenuDataRes = await reqAllMenuList(row.id);
  if (res) {
    menuArr.value = res.all_access;
    selectArr.value = findLeafKeys(menuArr.value, res.role_access);
  }
};
</script>
<style scoped></style>
