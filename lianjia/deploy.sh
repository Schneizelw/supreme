#!/bin/bash

function start() {
    hosts=(47.103.1.31 47.106.235.179)
    for host in ${hosts[@]}
        do
            result=$(curl http://$host:6800/schedule.json -d project=lianjia -d spider=lianjiacom)
            status=$(echo "$result" | jq '.status')
            if ["$status" == "ok"]
            then
                jobid=$(echo "$result" | jq '.jobid')
                echo jobid >> jobids.txt
            else
                echo "$result"
            fi
        done
}

function cancel() {
    hosts=(47.103.1.31 47.106.235.179)
    jobids=()
    n=${#hosts[@]}
    for jobid in "tail -n '$n' jobids.txt"
        do
            jobids[${#jobids[*]}]=jobid
        done
    for i in "${!hosts[@]}" 
        do
            result=$(curl http://${hosts[$i]}:6800/cancel.json -d project=lianjia -d job=${jobids[$i]})
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
}

function main() {
    case "$1" in
        "deploy_local") deploy_local;;
        "start_local") start_local;;
        "cancel_local") cancel_local $2;;
        "deploy") deploy;;
        "start") start;;
        "cancel") cancel;;
        *) usage;;
    esac
}
                                                        
main "$@"
