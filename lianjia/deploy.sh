#!/bin/bash

#hosts=(47.103.1.31 47.106.235.179)
hosts=(47.103.1.31)

function start() {
    for host in ${hosts[@]}
        do
            result=$(curl http://$host:6800/schedule.json -d project=lianjia -d spider=lianjiacom)
            status=$(echo "$result" | jq '.status')
            echo $status
            if [ "$status"x = "\"ok\""x ];then
                jobid=$(echo "$result" | jq '.jobid')
                jobid=$(echo $jobid | sed "s/\"//g")
                echo $jobid >> jobids.txt 
            fi
            echo "$result"
        done
}

function cancel() {
    jobids=()
    n=${#hosts[@]}
    for jobid in $(tail -n $n jobids.txt)
        do
            jobids[${#jobids[*]}]=$jobid
        done
    for i in "${!hosts[@]}" 
        do
            echo ${hosts[$i]}
            echo ${jobids[$i]}
            cmd="http://${hosts[$i]}:6800/cancel.json -d project=lianjia -d job=${jobids[$i]}"
            echo $cmd
            result=$(curl $cmd)
            echo "$result"
        done
}

function status() {
    for host in ${hosts[@]}
        do
            result=$(curl http://$host:6800/daemonstatus.json)
            echo "$result"
        done
}


function delproject() {
    for host in ${hosts[@]}
        do
            result=$(curl http://$host:6800/delproject.json -d project=lianjia)
            echo "$result"
        done
}

function deploy() {
    #部署到全部机器
    result=$(scrapyd-deploy -a)
    echo "$result" | jq '.status'
}

## local主要用于测试
function deploy_local() {
    #部署到vm1对应到的机器
    result=$(scrapyd-deploy vm1)
    echo "$result" | jq '.status'
    echo "$result"
}

function start_local() {
    #开启vm1中的spider
    result=$(curl http://47.106.235.179:6800/schedule.json -d project=lianjia -d spider=lianjiacom)
    echo "$result"
}

function cancel_local() {
    #取消vm1中的spider
    result=$(curl http://47.106.235.179:6800/cancel.json -d project=lianjia -d job=$1)
    echo "$result"
}

function usage() {
    echo "usage: sh $0 <command>"
    echo "  bash $0 deploy_local 将spider部署到本机测试"
    echo "  bash $0 start_local  开启本机的spider进行测试"
    echo "  bash $0 cancel_local jobid 取消在本机用于测试的spider"
    echo "  bash $0 deploy       将spider部署到所有服务器"
    echo "  bash $0 start        打开所有机器上的spider"
    echo "  bash $0 cancel       取消所有的spider"
    echo "  bash $0 stataus      查看任务状态"
    echo "  bash $0 delproject   删除项目"
}

function main() {
    case "$1" in
        "deploy_local") deploy_local;;
        "start_local") start_local;;
        "cancel_local") cancel_local $2;;
        "deploy") deploy;;
        "start") start;;
        "cancel") cancel;;
        "status") status;;
        "delproject") delproject;;
        *) usage;;
    esac
}
                                                        
main "$@"
