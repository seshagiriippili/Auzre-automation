node {
    // loading and running jenkins tasks
    workspace = pwd()

    project = "DAC625-DAC-Platform-Migration"
    playbook= "playbook.yml"
    task = "Hibernation"
    srcDir = "./Operations/Non-Prod/${task}"
    repositoryUrl = "https://github.com/NSWDAC/${project}.git"
    branch = "master"
    msg = "Spin up the choosen virtual machines"

    ok = '\u2705'
    no = '\u274C'

    stage 'Init Working Env'
    node() {
        sh "sudo /opt/bin/init.sh '${project}' '${task}'"
    }

    stage 'Check List'
    node() {
        echo "${ok} Check Workspace: ${workspace}/"
        sh "ls -ltrh /tmp/env/"
        echo "${ok} Check Ansible Availability"
        sh 'which ansible'
        echo "${ok} Check Ansible Version"
        sh 'ansible --version'
        echo "${no} Something's wrong..."
        echo '$&@*&%#)(*#@(*_)*&%#*^@&$)*'
        sh "cd '${srcDir}';ls -ltrhR"
    }

    stage 'Power On'
    node() {
        sh "cd '${srcDir}';sudo ansible-playbook --tags=\"poweron\" ${playbook}"
    }

    stage "Tasks Finalized"
    node() {
        sh "sudo /opt/bin/log.sh '${msg}'"
        sh "sudo /opt/bin/fin.sh ${project} ${task}"
    }

}

