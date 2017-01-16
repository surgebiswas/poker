/*
 * Copyright (C) 1999-2002
 *           Michael Maurer <mjmaurer@yahoo.com>
 *           Brian Goetz <brian@quiotix.com>
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
#ifndef __EVAL_JOKER_LOW_H__
#define __EVAL_JOKER_LOW_H__

#include <assert.h>
#include "handval_low.h"
#include "deck_joker.h"
#include "inlines/eval_low.h"

/*
 * Lowball evaluator with joker.  Assumes that n_cards >= 5.  
 * Performance could be improved by expanding the standard lowball evaluator,
 * rather than trying to manipulate the card mask so we can reuse the standard
 * lowball evaluator.  This would save a lot of bit extractions and redundant
 * bit operations (like computing ranks.)  
 */

static inline LowHandVal 
JokerDeck_Lowball_EVAL(JokerDeck_CardMask cards, int n_cards) {
  uint32 ranks, rank, ss, sh, sd, sc;
  StdDeck_CardMask sCards;

  JokerDeck_CardMask_toStd(cards, sCards);
  if (!JokerDeck_CardMask_JOKER(cards)) 
    return StdDeck_Lowball_EVAL(sCards, n_cards);

  ss = JokerDeck_CardMask_SPADES(cards);
  sc = JokerDeck_CardMask_CLUBS(cards);
  sd = JokerDeck_CardMask_DIAMONDS(cards);
  sh = JokerDeck_CardMask_HEARTS(cards);

  ranks = sc | ss | sd | sh;
  if (!(ranks & (1 << JokerDeck_Rank_ACE)))
    rank = 1 << JokerDeck_Rank_ACE;
  else 
    for (rank= (1 << JokerDeck_Rank_2); 
	 rank <= (1 << JokerDeck_Rank_KING); 
	 rank <<= 1) 
      if (!(ranks & rank))
	break;

  if (!(sc & rank)) 
    StdDeck_CardMask_SET_CLUBS(sCards, sc | rank);
  else if (!(sd & rank))
    StdDeck_CardMask_SET_DIAMONDS(sCards, sc | rank);
  else if (!(sh & rank))
    StdDeck_CardMask_SET_HEARTS(sCards, sh | rank);
  else if (!(ss & rank))
    StdDeck_CardMask_SET_SPADES(sCards, ss | rank);

  return StdDeck_Lowball_EVAL(sCards, n_cards);
}

#endif
