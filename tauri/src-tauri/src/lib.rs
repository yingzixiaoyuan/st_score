use log::{error, info, warn};
use std::env;

use killport::cli::Mode;
use killport::killport::{Killport, KillportOperations};
use killport::signal::KillportSignal;
use reqwest::Client;
use std::time::Duration;
use tauri::{Manager, WindowEvent};
use tauri_plugin_shell::ShellExt;
use tokio::time::sleep;

pub fn run() {
    env_logger::init();

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let splash_window = app.get_webview_window("splashscreen").unwrap();
            let main_window = app.get_webview_window("main").unwrap();
            let sidecar = app.shell().sidecar("st_score_analyzer").unwrap();

            tauri::async_runtime::spawn(async move {
                let (_rx, _child) = sidecar.spawn().expect("Failed to spawn sidecar");
                let client = Client::new();

                // 等待Streamlit服务器启动
                info!("等待Streamlit服务器启动...");
                let mut attempts = 0;
                let max_attempts = 60; // 最多等待30秒

                loop {
                    attempts += 1;
                    match client.get("http://localhost:8501").send().await {
                        Ok(response) if response.status().is_success() => {
                            info!("Streamlit服务器已就绪!");
                            sleep(Duration::from_millis(500)).await;
                            break;
                        }
                        _ => {
                            if attempts >= max_attempts {
                                error!("Streamlit服务器启动超时，请检查应用程序");
                                break;
                            }
                            warn!("Streamlit服务器尚未准备就绪，重试中... ({}/{})", attempts, max_attempts);
                            sleep(Duration::from_millis(500)).await;
                        }
                    }
                }

                // 加载Streamlit应用
                main_window
                    .eval("window.location.replace('http://localhost:8501');")
                    .expect("无法在主窗口中加载URL");

                sleep(Duration::from_millis(250)).await;
                splash_window.hide().unwrap();
                main_window.show().unwrap();
            });

            Ok(())
        })
        .on_window_event(|window, event| match event {
            #[allow(unused_variables)]
            WindowEvent::CloseRequested { api, .. } => {
                if window.label() == "splashscreen" {
                    info!("关闭请求 - 退出应用");
                    kill_score_analyzer(8501);
                    window.app_handle().exit(0);
                }
            }
            WindowEvent::Destroyed => {
                if window.label() == "main" {
                    info!("窗口已销毁 - 退出应用");
                    kill_score_analyzer(8501);
                    window.app_handle().exit(0);
                }
            }
            _ => {}
        })
        .run(tauri::generate_context!())
        .expect("运行Tauri应用程序时出错");
}

fn kill_score_analyzer(port: u16) {
    let killport = Killport;
    let mode = Mode::Auto;

    let target_killables = match killport.find_target_killables(port, mode) {
        Ok(killables) => killables,
        Err(err) => {
            error!("查找可终止进程时出错: {}", err);
            return;
        }
    };

    for killable in target_killables {
        // 终止包含应用名称的进程
        if killable.get_name().contains("st_score_analyzer") || 
           killable.get_name().contains("entrypoint") ||
           killable.get_name().contains("streamlit") {
            let signal: KillportSignal = "SIGKILL".parse().unwrap();

            if let Err(err) = killable.kill(signal) {
                error!("终止进程 {} 时出错: {}", killable.get_name(), err);
            } else {
                info!("已终止进程: {}", killable.get_name());
            }
        }
    }
}
