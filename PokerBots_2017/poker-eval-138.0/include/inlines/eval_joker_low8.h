/*
 * Copyright (C) 2002 Michael Maurer <mjmaurer@yahoo.com>
 *
 * This program gives you software freedom; you can copy, convey,
 * propagate, redistribute and/or modify this program under the terms of
 * the GNU General Public License (GPL) as published by the Free Software
 * Foundation (FSF), either version 3 of the License, or (at your option)
 * any later version of the GPL published by the FSF.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program in a file in the toplevel directory called "GPLv3".
 * If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef __EVAL_JOKER_LOW8_H__
#define __EVAL_JOKER_LOW8_H__

#include "handval_low.h"
#include "deck_joker.h"
#include "inlines/eval_joker_low.h"

static inline LowHandVal 
JokerDeck_Lowball8_EVAL(JokerDeck_CardMask cards, int n_cards) {
  LowHandVal loval;
  loval = JokerDeck_Lowball_EVAL(cards, n_cards);
  if (loval <= LowHandVal_WORST_EIGHT)
    return loval;
  else 
    return LowHandVal_NOTHING;
}

#endif
