Output "assets/terminal/quantum-shell-animated.gif"

Set FontSize 18
Set Width 1100
Set Height 260
Set Theme "Dracula"
Set Padding 16

# Uptime
Type "popdeuxrem@cid:~$ "
Sleep 300ms
Type "uptime"
Enter
Sleep 1200ms

# Disk usage
Type "popdeuxrem@cid:~$ "
Sleep 260ms
Type "df -h | head -5"
Enter
Sleep 1500ms

# Docker containers (with safe fallback)
Type "popdeuxrem@cid:~$ "
Sleep 260ms
Type "docker ps --format \"table {{.Names}}\t{{.Status}}\t{{.Ports}}\" || echo \"[docker inactive or unavailable]\""
Enter
Sleep 1700ms

# Kubernetes pods (with safe fallback)
Type "popdeuxrem@cid:~$ "
Sleep 260ms
Type "kubectl get pods --all-namespaces --context prod || echo \"[kube context not configured here]\""
Enter
Sleep 1800ms

# Basic system load
Type "popdeuxrem@cid:~$ "
Sleep 260ms
Type "ps aux --sort=-%cpu | head -5"
Enter
Sleep 1700ms

# Network sockets snapshot (short)
Type "popdeuxrem@cid:~$ "
Sleep 260ms
Type "ss -tulpn | head -5 || netstat -tulpn | head -5"
Enter
Sleep 1700ms

# Closing signature line
Type "popdeuxrem@cid:~$ "
Sleep 260ms
Type "echo \"[ systems artisan · infra meshes · observability rails ]\""
Enter
Sleep 1600ms

# Idle cursor at the end
Sleep 1000ms
