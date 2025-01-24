# File Share Integration

## 服务调用示例

### 1. 列出文件
```yaml
service: fileshare.list_files
data:
  path: "/config"
```

### 2. 上传文件
```yaml
service: fileshare.upload_file
data:
  path: "/config/test.txt"
  content: "Hello World"
```

### 3. 下载文件
```yaml
service: fileshare.download_file
data:
  path: "/config/test.txt"
```

### 4. 删除文件/文件夹
```yaml
service: fileshare.delete_file
data:
  path: "/config/test.txt"
```

### 5. 创建文件夹
```yaml
service: fileshare.create_directory
data:
  path: "/config/new_folder"
```

## 开发日志
- 2025-01-24: 初始版本发布
