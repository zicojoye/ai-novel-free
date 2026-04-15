#!/usr/bin/env node
/**
 * 启动脚本 - 自动检查依赖后启动前端服务
 * 已安装的依赖会跳过,没安装的会自动安装
 */

const { spawn, exec } = require('child_process');
const path = require('path');
const fs = require('fs');

function runCommand(command, args, description) {
    return new Promise((resolve, reject) => {
        console.log(`📝 ${description}...`);

        const proc = spawn(command, args, {
            stdio: 'inherit',
            shell: true
        });

        proc.on('close', (code) => {
            if (code === 0) {
                resolve();
            } else {
                reject(new Error(`${description} failed with code ${code}`));
            }
        });

        proc.on('error', (err) => {
            reject(err);
        });
    });
}

function checkDependencies() {
    console.log('=' .repeat(60));
    console.log('🔍 检查依赖...');
    console.log('=' .repeat(60));
    console.log();

    const frontendDir = __dirname;
    const nodeModulesPath = path.join(frontendDir, 'node_modules');

    if (fs.existsSync(nodeModulesPath)) {
        // 检查关键包
        const packageJson = require(path.join(frontendDir, 'package.json'));
        const dependencies = packageJson.dependencies || {};

        const keyPackages = ['react', 'react-dom', 'react-router-dom', 'zustand', 'axios'];
        let missing = [];

        for (const pkg of keyPackages) {
            const pkgPath = path.join(nodeModules, pkg);
            if (!fs.existsSync(pkgPath)) {
                missing.push(pkg);
            }
        }

        if (missing.length === 0) {
            console.log('✓ 所有关键依赖已安装');
            console.log();
            return Promise.resolve(true);
        } else {
            console.log(`⚠️  缺少依赖: ${missing.join(', ')}`);
            console.log();
        }
    } else {
        console.log('⚠️  node_modules不存在');
        console.log();
    }

    console.log('=' .repeat(60));
    console.log('📦 自动安装依赖...');
    console.log('=' .repeat(60));
    console.log();

    // 检查yarn是否可用
    return exec('yarn --version', (err, stdout) => {
        if (!err && stdout) {
            console.log('✓ 使用yarn安装');
            return runCommand('yarn', ['install'], 'yarn install');
        } else {
            console.log('✓ 使用npm安装');
            return runCommand('npm', ['install'], 'npm install');
        }
    }).then(() => {
        console.log();
        console.log('✅ 依赖安装完成!');
        console.log();
        return true;
    }).catch(err => {
        console.log('\n❌ 依赖安装失败');
        console.log('\n请手动运行: npm install');
        return Promise.reject(err);
    });
}

function startDevServer() {
    console.log('=' .repeat(60));
    console.log('🚀 启动AI Novel Platform前端服务...');
    console.log('=' .repeat(60));
    console.log();

    // 检查yarn是否可用
    exec('yarn --version', (err, stdout) => {
        if (!err && stdout) {
            console.log('✓ 使用yarn启动');
            const devServer = spawn('yarn', ['dev'], {
                stdio: 'inherit',
                shell: true
            });

            devServer.on('error', (err) => {
                console.error('\n❌ 启动失败:', err.message);
                process.exit(1);
            });

            process.on('SIGINT', () => {
                console.log('\n\n🛑 服务已停止');
                devServer.kill();
                process.exit(0);
            });
        } else {
            console.log('✓ 使用npm启动');
            const devServer = spawn('npm', ['run', 'dev'], {
                stdio: 'inherit',
                shell: true
            });

            devServer.on('error', (err) => {
                console.error('\n❌ 启动失败:', err.message);
                process.exit(1);
            });

            process.on('SIGINT', () => {
                console.log('\n\n🛑 服务已停止');
                devServer.kill();
                process.exit(0);
            });
        }
    });
}

function main() {
    console.log('\n' + '=' .repeat(60));
    console.log('🎯 AI Novel Platform 前端启动器');
    console.log('=' .repeat(60));
    console.log();

    checkDependencies()
        .then(() => {
            startDevServer();
        })
        .catch(err => {
            console.error('\n❌ 依赖检查失败,无法启动服务');
            console.error(err.message);
            process.exit(1);
        });
}

main();
