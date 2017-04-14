"""
Basic utilities for
"""
############
# Standard #
############
import logging
import threading
###############
# Third Party #
###############


##########
# Module #
##########


def destroy_on_exit(proc, tmp):
    """
    Destory temporary files on process completion
    """
    #Worker
    def wait(proc, tmp):
        proc.wait()
        list(map(lambda x : x.close(), tmp))
    #Run
    thread = threading.Thread(target=wait, args=(proc, tmp))
    thread.start()
    return thread
