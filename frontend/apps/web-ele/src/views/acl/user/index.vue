<template>
  <el-card style="height: 80px">
    <el-form :inline="true" class="form">
      <el-form-item label="用户名:">
        <el-input placeholder="请你输入搜索用户名" v-model="keyword"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" size="default">搜索</el-button>
        <el-button type="primary" size="default">重置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
  <el-card style="margin: 10px 0px">
    <el-button type="primary" size="default" @click="addUser"
      >添加用户</el-button
    >
    <el-button type="primary" size="default">批量删除</el-button>
    <!-- table展示用户信息 -->
    <el-table style="margin: 10px 0px" border :data="userArr">
      <el-table-column type="selection" align="center"></el-table-column>
      <el-table-column label="#" align="center" type="index"></el-table-column>
      <el-table-column
        label="用户名"
        align="center"
        prop="username"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column
        label="手机号"
        align="center"
        prop="user_phone"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column
        label="邮箱"
        align="center"
        prop="user_email"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column
        label="状态"
        align="center"
        prop="user_status"
        show-overflow-tooltip
      >
        <template #="{ row }">
          <el-tag :type="row.user_status ? 'success' : 'danger'">{{
            row.user_status ? '启用' : '禁用'
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="300px" align="center">
        <template #="{ row }">
          <el-popconfirm
            :title="`你确定要${!row.user_status ? '启用' : '禁用'}${row.username}?`"
            width="260px"
          >
            <template #reference>
              <el-button type="primary" size="small" plain>{{
                !row.user_status ? '启用' : '禁用'
              }}</el-button>
            </template>
          </el-popconfirm>
          <el-popconfirm
            :title="`你确定要删除${row.username}?`"
            width="260px"
            @confirm="deleteUser(row.id)"
          >
            <template #reference>
              <el-button type="danger" size="small" plain>删除</el-button>
            </template>
          </el-popconfirm>
          <el-button type="primary" size="small" plain>编辑</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="pageNo"
      v-model:page-size="pageSize"
      :page-sizes="[5, 7, 9, 11]"
      :background="true"
      layout="prev, pager, next, jumper,->,sizes,total"
      :total="total"
      @current-change="getHasUser"
      @size-change="hander"
    />
  </el-card>

  <el-drawer v-model="drawer">
    <template #header>
      <h4>添加用户</h4>
    </template>
    <template #default>
      <el-form :model="userParams" :rules="rules" ref="formRef">
        <el-form-item label="用户姓名" prop="username">
          <el-input
            placeholder="请您输入用户姓名"
            v-model="userParams.username"
          ></el-input>
        </el-form-item>
        <el-form-item label="用户密码" prop="password">
          <el-input
            placeholder="请您输入用户密码"
            v-model="userParams.password"
          ></el-input>
        </el-form-item>
      </el-form>
    </template>
    <template #footer>
      <div style="flex: auto">
        <el-button type="primary" @click="cancel">取消</el-button>
        <el-button type="primary" @click="save">确定</el-button>
      </div>
    </template>
  </el-drawer>
</template>
<script lang="ts" setup>
// 引入
import {
  ElCard,
  ElButton,
  ElTable,
  ElTableColumn,
  ElPagination,
  ElMessage,
  ElDrawer,
  ElForm,
  ElFormItem,
  ElInput,
  ElTag,
  ElPopconfirm,
} from 'element-plus';
import { ref, onMounted, nextTick } from 'vue';
import type { UserListItem, UserListResp, User } from '#/api';
import { reqUserList, reqAddOrUpdateUser, reqRemoveUser } from '#/api';

const userArr = ref<UserListItem[]>([]);

const total = ref<number>(0);
const pageNo = ref<number>(1);
const pageSize = ref<number>(5);
const keyword = ref<string>('');

onMounted(() => {
  getHasUser();
});
const getHasUser = async (pager = 1) => {
  pageNo.value = pager;
  let result: UserListResp = await reqUserList(
    pageNo.value,
    pageSize.value,
    keyword.value,
  );
  if (result.total > 0) {
    total.value = result.total;
    userArr.value = result.items;
  }
};

const hander = () => {
  getHasUser(pageNo.value);
};
const formRef = ref<any>(null);
const drawer = ref<boolean>(false);
const userParams = ref<User>({
  username: '',
  password: '',
});

const addUser = () => {
  drawer.value = true;
  Object.assign(userParams, {
    id: 0,
    username: '',
    password: '',
  });
  nextTick(() => {
    formRef.value.clearValidate('username');
    formRef.value.clearValidate('nickname');
    formRef.value.clearValidate('password');
  });
};

const cancel = () => {
  drawer.value = false;
};
const save = async () => {
  await formRef.value.validate();
  let result: any = await reqAddOrUpdateUser(userParams.value);
  if (result !== null) {
    drawer.value = false;
    ElMessage({
      type: 'success',
      message: userParams.value.id ? '更新成功' : '添加成功',
    });
    getHasUser(pageNo.value);
  } else {
    drawer.value = false;
    ElMessage({
      type: 'error',
      message: userParams.value.id ? '更新失败' : '添加失败',
    });
  }
};

const validatorUsername = (rule: any, value: any, callBack: any) => {
  if (value.trim().length >= 5) {
    callBack();
  } else {
    callBack(new Error('用户名字至少五位'));
  }
};
const validatorPassword = (rule: any, value: any, callBack: any) => {
  if (value.trim().length >= 6) {
    callBack();
  } else {
    callBack(new Error('用户密码至少六位'));
  }
};

const rules = {
  username: [{ required: true, trigger: 'blur', validator: validatorUsername }],
  password: [{ required: true, trigger: 'blur', validator: validatorPassword }],
};

const deleteUser = async (userId: number) => {
  let result: any = await reqRemoveUser(userId);
  if (result !== null) {
    ElMessage({ type: 'success', message: '删除成功' });
    getHasUser(userArr.value.length > 1 ? pageNo.value : pageNo.value - 1);
  }
};
</script>

<style scoped></style>
