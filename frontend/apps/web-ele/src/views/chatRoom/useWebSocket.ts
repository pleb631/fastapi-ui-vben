import { ref, onBeforeUnmount } from 'vue';

type WsAction = 'push_msg' | 'pull_msg' | 'refresh_online_user';
interface WsBase {
  action: WsAction;
  [k: string]: any;
}

export function useWebSocket(opts: {
  baseURL: string; // 如: ws://127.0.0.1:8000
  path?: string; // 默认 /test
  uType: number; // 你的 u_type
  token: string; // 你的 token，走 subprotocol
  autoReconnect?: boolean;
  reconnectDelayMs?: number;
}) {
  const {
    baseURL,
    path = '/test',
    uType,
    token,
    autoReconnect = true,
    reconnectDelayMs = 1500,
  } = opts;

  interface UserBase {
    id: number;
    username: string;
    avatar?: string;
  }

  const ws = ref<WebSocket | null>(null);
  const isOpen = ref(false);
  const onlineUsers = ref<UserBase[]>([]);
  const messages = ref<any[]>([]);
  let reconnectTimer: number | null = null;
  let heartbeatTimer: number | null = null;
  let manuallyClosed = false;
  let shouldReconnect = !!autoReconnect;

  const url = `${baseURL.replace(/\/$/, '')}${path}?u_type=${encodeURIComponent(
    String(uType),
  )}`;

  const connect = () => {
    if (
      ws.value &&
      (ws.value.readyState === WebSocket.OPEN ||
        ws.value.readyState === WebSocket.CONNECTING)
    )
      return;
    ws.value = new WebSocket(url, [token]);

    ws.value.onopen = () => {
      isOpen.value = true;
      if (reconnectTimer) {
        clearTimeout(reconnectTimer);
        reconnectTimer = null;
      }

      heartbeatTimer = window.setInterval(() => {
        try {
          ws.value?.send(JSON.stringify({ action: 'ping', t: Date.now() }));
        } catch {}
      }, 30000);
    };

    ws.value.onmessage = (ev) => {
      try {
        const data: WsBase = JSON.parse(ev.data);
        switch (data.action) {
          case 'refresh_online_user':
            // 后端返回的数据是 {action:'refresh_online_user', data:[{id,username},...]}
            onlineUsers.value = Array.isArray(data.data) ? data.data : [];
            break;
          case 'pull_msg':
            // 群发下行消息
            messages.value.push(data);
            break;
          default:
            // 其他类型，按需处理/记录
            messages.value.push({ action: 'unknown', raw: data });
        }
      } catch (e) {
        console.error('WS message parse error:', e, ev.data);
      }
    };

    ws.value.onclose = () => {
      isOpen.value = false;
      cleanupTimers();
      ws.value = null;
      if (!manuallyClosed && shouldReconnect) {
        reconnectTimer = window.setTimeout(
          connect,
          reconnectDelayMs,
        ) as unknown as number;
      }
      manuallyClosed = false;
    };

    ws.value.onerror = () => {
      ws.value?.close();
    };
  };

  const cleanupTimers = () => {
    if (heartbeatTimer) {
      window.clearInterval(heartbeatTimer);
      heartbeatTimer = null;
    }
  };

  const close = (
    code = 1000,
    reason = 'client closed',
    disableReconnect = true,
  ) => {
    if (disableReconnect) shouldReconnect = false;
    manuallyClosed = true;
    ws.value?.close();
    cleanupTimers();
    if (ws.value) {
      if (ws.value.readyState === WebSocket.OPEN) {
        ws.value.close(code, reason);
      } else if (ws.value.readyState === WebSocket.CONNECTING) {
        ws.value.addEventListener('open', () => ws.value?.close(code, reason), {
          once: true,
        });
      }
    }
    onlineUsers.value = [];
  };

  const sendJson = (payload: WsBase | Record<string, any>) => {
    if (!ws.value || ws.value.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket 未连接');
    }
    ws.value.send(JSON.stringify(payload));
  };

  onBeforeUnmount(close);

  return {
    // state
    isOpen,
    onlineUsers,
    messages,
    // api
    connect,
    close,
    sendJson,
  };
}
