/*
*   Copyright (C) 2017  Paul Springer (springer@aices.rwth-aachen.de)
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU Lesser General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


#ifndef TCL_CONTRACT_H
#define TCL_CONTRACT_H

/// \page pg_contract Tensor Contraction
///
/// \section sec_contract Tensor Contraction
/// A tensor contraction is the generalization of a matrix-matrix multiplication to multiple dimensions

#include <list>
#include <vector>
#include <string>
#include <memory>
#include <numeric>
#include <functional>
#include <stdio.h>
#include <stdlib.h>

#include "types.h"
#include "tensor.h"

namespace tcl{

   template<typename floatType>
   error multiply(const floatType alpha, const Tensor<floatType> *A,
                                         const Tensor<floatType> *B, 
                  const floatType beta,        Tensor<floatType> *C, int useTTGT = 1);
}

#endif