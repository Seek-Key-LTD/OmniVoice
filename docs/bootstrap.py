#!/usr/bin/env python3
"""OmniVoice Colab 一键启动脚本"""
import subprocess, os, time

def run(cmd, hide=True):
    subprocess.run(cmd, shell=True, capture_output=hide, text=True)

print("⚡ 安装 OmniVoice...")
run("pip install -q omnivoice")

print("🔑 配置 SSH...")
run("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq openssh-server cloudflared > /dev/null 2>&1")
run("echo 'root:3131' | chpasswd")
run("mkdir -p /var/run/sshd")
run("sed -i 's/^#\\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config")
run("sed -i 's/^#\\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config")
run("service ssh start")

# raccoon 公钥
key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICDDIVZS/Lexzu26ur8KK+Uky5wkrRIVRaFH0sw2GOso"
run(f"mkdir -p ~/.ssh && echo '{key}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys")

print("🌐 启动 Cloudflare 隧道...")
run("nohup cloudflared tunnel --url ssh://localhost:22 > /tmp/cloudflared.log 2>&1 &")
time.sleep(3)

print("\n✅ 环境就绪！")
print("   SSH:  ssh colab (密码 3131)")
print("")
print("🚀 启动 Gradio...")
os.system("omnivoice-demo --share")
