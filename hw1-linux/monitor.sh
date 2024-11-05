#!/bin/bash

MONITOR_INTERVAL=60
OUTPUT_DIR="./monitoring_logs"
mkdir -p "$OUTPUT_DIR"

PID_FILE="/tmp/disk_monitor.pid"

start_monitoring() {
    if [ -f "$PID_FILE" ]; then
        echo "Monitoring is already running with PID $(cat $PID_FILE)."
        exit 1
    fi

    (
        while true; do
            current_datetime=$(date +"%Y-%m-%d_%H-%M-%S")
            current_date=$(date +"%Y-%m-%d")

            csv_file="$OUTPUT_DIR/disk_usage_$current_date.csv"

            if [ ! -f "$csv_file" ]; then
                echo "Timestamp,Filesystem,Used,Available,Use%,FreeInodes,UsedInodes" > "$csv_file"
            fi

            df_output=$(df -h)
            inode_output=$(df -i)

            echo "$df_output" | tail -n +2 | while read -r line; do
                filesystem=$(echo $line | awk '{print $1}')
                used=$(echo $line | awk '{print $3}')
                available=$(echo $line | awk '{print $4}')
                use_percentage=$(echo $line | awk '{print $5}')

                inode_line=$(echo "$inode_output" | grep "^$filesystem")
                free_inodes=$(echo $inode_line | awk '{print $4}')
                used_inodes=$(echo $inode_line | awk '{print $3}')

                echo "$current_datetime,$filesystem,$used,$available,$use_percentage,$free_inodes,$used_inodes" >> "$csv_file"
            done

            sleep $MONITOR_INTERVAL
        done
    ) &

    echo $! > "$PID_FILE"
    echo "Monitoring started with PID $!"
}

stop_monitoring() {
    if [ -f "$PID_FILE" ]; then
        pid=$(cat "$PID_FILE")
        kill "$pid"
        rm "$PID_FILE"
        echo "Monitoring stopped."
    else
        echo "No monitoring process is running."
    fi
}

status_monitoring() {
    if [ -f "$PID_FILE" ]; then
        echo "Monitoring is running with PID $(cat $PID_FILE)."
    else
        echo "Monitoring is not running."
    fi
}

case "$1" in
    START)
        start_monitoring
        ;;
    STOP)
        stop_monitoring
        ;;
    STATUS)
        status_monitoring
        ;;
    *)
        echo "Usage: $0 {START|STOP|STATUS}"
        exit 1
        ;;
esac