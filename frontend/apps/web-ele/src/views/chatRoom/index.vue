<template>
  <div class="p-4 space-y-4">
    <div class="flex items-center gap-2">
      <el-button
        :disabled="isOpen"
        @click="connect"
        type="primary"
      >
        连接
      </el-button>
      <el-button @click="close" type="default">
        断开
      </el-button>
      <span :class="isOpen ? 'text-green-600' : 'text-red-600'" class="text-sm">
        {{ isOpen ? '已连接' : '未连接' }}
      </span>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="md:col-span-2 border rounded p-3">
        <div class="font-medium mb-2">消息</div>
        <div class="h-64 overflow-auto border rounded p-2 space-y-2">
          <div v-for="(m, idx) in messages" :key="idx" class="text-sm">
            <pre class="whitespace-pre-wrap break-words">用户{{m.user}}: {{ m.content }}</pre>
          </div>
        </div>
        <div class="mt-3 flex gap-2">
          <el-input
            v-model="input"
            placeholder="输入消息内容..."
            @keyup.enter="send"
            class="flex-1"
            :style="{ backgroundColor: '#333', color: '#fff' }"
          />
          <el-button type="primary" @click="send">
            发送
          </el-button>
        </div>
      </div>

      <div class="border rounded p-3">
        <div class="font-medium mb-2">在线用户</div>
        <ul class="space-y-1 text-sm">
          <li v-for="u in onlineUsers" :key="u.id" class="flex items-center gap-2">
            <el-avatar :src="u.avatar" size="small" />
            {{ u.username }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useWebSocket } from './useWebSocket'
import { ElButton, ElInput, ElAvatar } from 'element-plus'

// 按实际情况填
const token = JSON.parse(localStorage.getItem("vben-web-ele-5.5.9-dev-core-access") as string).accessToken.replace(/^Bearer\s+/i, '') || ''

const uType = 1
const baseURL = "ws://127.0.0.1:15555"
// 如果后端和前端不在同一域名/端口，就换成后端地址：例如 ws://127.0.0.1:8000

const { isOpen, onlineUsers, messages, connect, close, sendJson } = useWebSocket({
  baseURL,
  path: '/test',
  uType,
  token,
})


const input = ref('')

function send() {
  if (!input.value.trim()) return
  // 后端 on_receive 里期待的是 { action: 'push_msg', ... }
  // 它会转成下行的 { action: 'pull_msg', user, ... }
  try {
    sendJson({
      action: 'push_msg',
      content: input.value.trim(),
      t: Date.now(),
    })
    input.value = ''
  } catch (e) {
    console.error(e)
    alert('尚未连接或发送失败')
  }
}
</script>

<style scoped>

.bg-gray-900 {
  background-color: #1a202c;
}

.text-white {
  color: white;
}

.el-input {
  background-color: #333;
  color: #fff;
}

.el-button {
  transition: background-color 0.3s ease;
}

.el-button:hover {
  background-color: #3b82f6;
}
</style>
