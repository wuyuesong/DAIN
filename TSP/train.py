DEBUG_MODE = True
USE_CUDA = True
# USE_CUDA = not DEBUG_MODE
CUDA_DEVICE_NUM = 0

# Path Config
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "..")
sys.path.insert(0, "../..")
import logging
from DAIN.utils.utils import create_logger, copy_all_src
from DAIN.TSP.TSPTrainer import TSPTrainer as Trainer


##########################################################################################
# parameters

b = os.path.abspath(".").replace('\\', '/')

mode = 'train'
training_data_path = b+"/data/train_TSP100_n100w.txt"
append_information = [True, True, True, False, True, True, False, False, False, False, False]   
#                      0      1     2    3      4      5      6      7      8      9     10
# 0.distance_to_current,  1.average_distance_to_unvisited,  2.std_dev_distance_to_unvisited,  3.distance_to_destination, 4.sin_to_destination, 
# 5.cos_to_destination,   6.average_distance_to_all         7.std_dev_distance_to_all         8.first_node               9 knn_mean                    10. knn_std

env_params = {
    'data_path':training_data_path,
    'mode': mode,
    'sub_path': False,
    'replace_size': 4,
    'append_information': append_information,
    'pomo_size': 16,
    'aggregation_nums': 50,
}

model_params = {
    'mode': mode,
    'embedding_dim': 128,
    'sqrt_embedding_dim': 128**(1/2),
    'decoder_layer_num':3,
    'qkv_dim': 16,
    'head_num': 8,
    'ff_hidden_dim': 512,
    'append_information': append_information,
}

optimizer_params = {
    'optimizer': {
        'lr': 1e-4,
        # 'lr': 1e-5,
        'weight_decay': 1e-6
                 },
    'scheduler': {
        'milestones': [1 * i for i in range(1, 200)],
        'gamma': 0.97
        # 'milestones': [501,],
        # 'gamma': 0.1
                 }
}

trainer_params = {
    'use_cuda': USE_CUDA,
    'cuda_device_num': CUDA_DEVICE_NUM,
    'epochs': 150,
    'train_episodes': 1000000,
    'train_batch_size': 1024,
    'loop_in_one_epoch': 1,
    'beam_size': 100,
    'keep_threshold': 2,
    'logging': {
        'model_save_interval': 1,
        'img_save_interval': 3000,
        'log_image_params_1': {
            'json_foldername': 'log_image_style',
            'filename': 'style_tsp_100.json'
               },
        'log_image_params_2': {
            'json_foldername': 'log_image_style',
            'filename': 'style_loss_1.json'
               },
        'log_image_params_3': {
            'json_foldername': 'log_image_style',
            'filename': 'style_tsp_100.json'
               },
               },
    'model_load': {
        'enable': False,  # enable loading pre-trained model
        'path': './result/20240723_220249_train',  # directory path of pre-trained model and log files saved.
        'epoch': 40,  # epoch version of pre-trained model to laod.
                  },
    }


logger_params = {
    'log_file': {
        'desc': 'train',
        'filename': 'log.txt'
    }
}

##########################################################################################
# main

def main():
    if DEBUG_MODE:
        _set_debug_mode()

    create_logger(**logger_params)
    _print_config()

    trainer = Trainer(env_params=env_params,
                      model_params=model_params,
                      optimizer_params=optimizer_params,
                      trainer_params=trainer_params,)

    copy_all_src(trainer.result_folder)

    trainer.run()


def _set_debug_mode():
    global trainer_params

    trainer_params['epochs'] = 100
    trainer_params['train_batch_size'] = 256
    trainer_params['step_size'] = 256
    trainer_params['beam_size'] = 4
    trainer_params['problem_size'] = 100
    trainer_params['knn'] = 30
    env_params['max_replace_ratio'] = 0.125
    env_params['min_replace_ratio'] = 0.125

    # trainer_params['epochs'] = 2
    # # trainer_params['train_episodes'] = 128
    # trainer_params['train_batch_size'] = 5
    # trainer_params['beam_size'] = 2
    # # trainer_params['epochs'] = 200
    # # trainer_params['train_episodes'] = 200000
    # # trainer_params['train_batch_size'] = 64
    # trainer_params['problem_size'] = 20
    # trainer_params['knn'] = 10
    # valid_params['valid_batch_size'] = 5
    # env_params['replace_size'] = 5
    # model_params['global_information'] = global_information



def _print_config():
    logger = logging.getLogger('root')
    
    logger.info('DEBUG_MODE: {}'.format(DEBUG_MODE))
    logger.info('USE_CUDA: {}, CUDA_DEVICE_NUM: {}'.format(USE_CUDA, CUDA_DEVICE_NUM))
    [logger.info(g_key + "{}".format(globals()[g_key])) for g_key in globals().keys() if g_key.endswith('params')]


##########################################################################################

if __name__ == "__main__":

    main()

