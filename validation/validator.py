import os
import json
from typing import List, Tuple
import const

class Validator():
  def __init__(self, filepath: str, lab_data: list, exercise_start: float, exercise_end: float):
    if not os.path.exists(filepath):
      raise FileNotFoundError(f"file '{filepath}' does not exist")
    self.lab_data = lab_data

    with open(filepath) as f:
      mobile_data = json.load(f)
    self.mobile_data = list(filter(
      lambda kp: kp.get('timestamp') > exercise_start and kp.get('timestamp') < exercise_end,
      mobile_data
    ))

  def zip(self) -> List[Tuple[dict, dict]]:
    j = 0
    zipped = []
    for mpose in self.mobile_data:
      best_pair = None
      best_time_diff = None
      while j < len(self.lab_data):
        kpose = self.lab_data[j]
        time_diff = abs(mpose.get('timestamp') - kpose.get('timestamp'))
        if time_diff < const.THRESHOLD:
          if not best_time_diff or time_diff < best_time_diff:
            # best match for this mkp so far.
            best_time_diff = time_diff
            best_pair = (kpose, mpose)
          if kpose.get('timestamp') > mpose.get('timestamp'):
            # no better matches to be found after this point
            if best_pair:
              zipped.append(best_pair)
            if best_time_diff == time_diff:
              # move to next lab pose if this one was used
              j += 1
            break
        elif kpose.get('timestamp') > mpose.get('timestamp'):
          break
        j += 1

    # record length for logging + return zipped list
    self.zipped_length = len(zipped)
    return zipped

  def log(self) -> None:
    '''Print logging information collected during validation process'''
    print('\nVALIDATION LOG')
    print('==============')
    print(f'{self.zipped_length} mobile data poses matched from a potential {len(self.mobile_data)} ({int(self.zipped_length / len(self.mobile_data) * 100)}%)')
    print('==============\n')

  def validate(self) -> None:
    self.log()

