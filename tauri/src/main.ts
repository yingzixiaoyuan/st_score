// 学生成绩分析器 - Tauri 前端入口
import { invoke } from "@tauri-apps/api/core";

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🎯 学生成绩分析器桌面应用已启动');
    
    // 这里可以添加任何需要的前端逻辑
    // 目前保持简单，只是一个包装器
    
    try {
        // 可以与Tauri后端通信的示例
        console.log('✅ Tauri API 可用');
    } catch (error) {
        console.warn('⚠️ Tauri API 初始化失败:', error);
    }
});

// 导出一些基础功能（如果需要）
export {};
