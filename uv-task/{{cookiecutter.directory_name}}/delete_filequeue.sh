#bin/bash
filepath=$(echo $TASKQUEUE_PATH | sed 's|^fq://||')
rm -r $filepath