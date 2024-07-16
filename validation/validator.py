import os
import json
from typing import List, Tuple

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
    for i, mkp in enumerate(self.mobile_data):
      while j < len(self.lab_data):
        lkp = self.lab_data[j]
        if abs(mkp.get('timestamp') - lkp.get('timestamp')) < const.THRESHOLD:
          zipped.append((lkp, mkp))
        elif lkp.get('timestamp') > mkp.get('timestamp'):
          break
        j += 1
    return zipped

