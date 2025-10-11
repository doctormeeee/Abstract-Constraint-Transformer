#===- util.path_config.py ----ACT Path Configuration ---------------------#
#
#                 ACT: Abstract Constraints Transformer
#
# Copyright (C) <2025->  ACT Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Purpose:
#   Python path configuration utilities for the Abstract Constraints Transformer
#   (ACT), ensuring proper module imports and path resolution across the
#   verification framework components.
#
#===----------------------------------------------------------------------===#

import os
import sys
from typing import Any, Optional, Tuple


def setup_act_paths() -> str:
    """Set up ACT project paths for proper module imports."""
    current_file = os.path.abspath(__file__)
    act_root = os.path.dirname(os.path.dirname(current_file))  # go up from util/ to act/
    if act_root not in sys.path:
        sys.path.insert(0, act_root)
    return act_root


def get_project_root() -> str:
    """Get the project root directory (parent of act/)."""
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    return project_root


# Set up paths
act_root = setup_act_paths()
project_root = get_project_root()


def ensure_gurobi_license() -> Optional[str]:
    """Ensure GRB_LICENSE_FILE is set to a valid Gurobi license file."""
    existing_license = os.environ.get('GRB_LICENSE_FILE')
    if existing_license:
        license_path = os.path.abspath(existing_license)
        print(f"[ACT] Using existing Gurobi license: {license_path}")
        return license_path

    if 'ACTHOME' in os.environ:
        acthome = os.environ['ACTHOME']
        print(f"[ACT] Using ACTHOME environment variable: {acthome}")
        license_path = os.path.abspath(os.path.join(acthome, 'gurobi', 'gurobi.lic'))
        if os.path.exists(license_path):
            os.environ['GRB_LICENSE_FILE'] = license_path
            print(f"[ACT] Gurobi license found and set: {license_path}")
            return license_path
        else:
            print(f"[WARN] Gurobi license not found at: {license_path}")
            print(f"[INFO] Please ensure gurobi.lic is placed in: {os.path.dirname(license_path)}")

    print(f"[ACT] Auto-detecting project root from path_config")
    license_path = os.path.abspath(os.path.join(project_root, 'gurobi', 'gurobi.lic'))
    if os.path.exists(license_path):
        os.environ['GRB_LICENSE_FILE'] = license_path
        print(f"[ACT] Gurobi license found and set: {license_path}")
        return license_path

    print(f"[WARN] Gurobi license not found at: {license_path}")
    print(f"[INFO] Please ensure gurobi.lic is placed in: {os.path.dirname(license_path)}")
    return None


def import_gurobi(ensure_license: bool = False) -> Tuple[bool, Optional[Any], Optional[Any]]:
    """Attempt to import Gurobi and return availability with module handles."""
    if ensure_license:
        ensure_gurobi_license()

    try:
        import gurobipy as gp  # type: ignore[import-not-found]
        from gurobipy import GRB  # type: ignore[import-not-found]
        return True, gp, GRB
    except ImportError:
        print("Warning: Gurobi not available. HybridZonotope modules will use alternative solvers.")
        return False, None, None


def configure_torch_print(linewidth: int = 500,
                          threshold: int = 10000,
                          sci_mode: bool = False,
                          precision: int = 4) -> None:
    """Configure default Torch print options for consistent tensor logging."""
    import torch

    torch.set_printoptions(
        linewidth=linewidth,
        threshold=threshold,
        sci_mode=sci_mode,
        precision=precision
    )
