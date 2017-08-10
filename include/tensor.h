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


#ifndef TCL_TENSOR_H
#define TCL_TENSOR_H

/// \class
/// Tensor 
///
/// \page pg_tensor Tensor 
///
/// \section sec_tensor Tensor 
/// A tensor is a symbolic representation of a tensor

#include <list>
#include <vector>
#include <string>
#include <memory>
#include <numeric>
#include <functional>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include <omp.h>

#include "types.h"
#include "utils.h"

namespace tcl{

   /*!
    * This class represents a tensor. 
    * A tensor stores information about its dimensionality, size and a pointer
    * to its data.
    */

   template<typename floatType>
   class Tensor
   {
      public:
         Tensor( const std::vector<sizeType> &size, 
                 const std::vector<sizeType> &outerSize = {},
                 const indicesType &indices = {},
                 const std::vector<sizeType> &offsets = {},
                 floatType * data = nullptr );

         Tensor( const std::vector<sizeType> &size, 
                 floatType * data ) : Tensor( size, size, {}, {}, data ) {}

         Tensor( const Tensor& other ) : _data(other._data), 
                                         _size(other._size),
                                         _outerSize(other._outerSize),
                                         _indices(other._indices),
                                         _offsets(other._offsets),
                                         _isSubtensor(false) {}
         ~Tensor() { 
//            if( (!_isSubtensor) && _data != nullptr)
//               free(_data);
         }

         /**
          * Return a subtensor that is that is spanned by the indices. For
          * example, if this tensor is A_{m,n,k} \in \mathbb{R}^{M \times N \times K}}
          * and indices = {m,k}, then this function would return the subtensor 
          * A_{m,k} \in \mathbb{R}^{M \times K} with a change outer size for the 
          * m-dimension = M * N as oppossed to just M.
          *
          * \param[in] indices Indices of the desired subtensor. The indices
          *   have to be in the same order as they appear in the parent tensor.
          *   Moreover: 1 <= indices.size() <= this.getDim().
          * \param[in] size Size of each dimension of the subtensor. size.size() == indices.size().
          */
         Tensor<floatType> getSubTensor( 
               const indicesType &indices,  
               const std::vector<sizeType> &size = {}) const;

         /**
          * Calculate the product of the sizes of the indices specified by 'indices'
          * \return Product of the sizes of the specified indices
          */
         sizeType getTotalSize( const indicesType &indices = {} ) const; 

         /**
          * \return The stride of the specified index
          */
         sizeType getStride( const std::string &idx ) const;

         /**
          * \return The size of the dimension corresponding to the specified index
          */
         sizeType getSize( const std::string &idx ) const;

         const std::vector<sizeType>& getSize() const { return _size; }
         const std::vector<sizeType>& getOuterSize() const { return _outerSize; }
         const indicesType& getIndices() const { return _indices; }
         int getDim() const { return _size.size(); }
         floatType* getData() const { 
            sizeType offset = 0;
            sizeType stride = 1;
            for(int i=0; i < _outerSize.size(); ++i){
               offset += stride * _offsets[i];
               stride *= _outerSize[i];
            }

            return &_data[offset]; 
         }
         void setData(floatType *data) { _data = data; }

         Tensor* operator[] (const std::string &&indices){
            split(indices, ',', _indices);
            return this;
         }
         Tensor* operator[] (const std::string &indices){
            split(indices, ',', _indices);
            return this;
         }

         void print();

      private:
         Tensor() {};

         /***************************************
          * private member functions
          ***************************************/

         floatType * _data;
         std::vector<sizeType> _size; 
         std::vector<sizeType> _outerSize; 
         indicesType _indices;
         std::vector<sizeType> _offsets; 
         bool _isSubtensor;
   };
}

#endif