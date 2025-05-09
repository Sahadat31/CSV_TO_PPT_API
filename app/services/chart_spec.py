from typing import Literal, Dict, Any

ChartType = Literal["time_series", "bar", "histogram"]

ChartSpec = Dict[str, Any]
# e.g.
# {
#   "type": "bar",
#   "x": "region",
#   "y": "units_sold",
#   "max_categories": 5
# }
