/*
 *  Copyright 2006 Michael Maurer <mjmaurer@yahoo.com>, 
 *                 Brian Goetz <brian@quiotix.com>, 
 *                 Loic Dachary <loic@dachary.org>, 
 *                 Tim Showalter <tjs@psaux.com>
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
#include <stdio.h>

#include "poker_defs.h"
#include "handval_low.h"

#define CARD_TO_RANK(c) ((c) == StdDeck_Rank_2 ? StdDeck_Rank_ACE : (c-1))

int 
LowHandVal_toString(LowHandVal hv, char *outString) {
  char *p = outString;
  int htype = HandVal_HANDTYPE(hv);

  if (hv == LowHandVal_NOTHING) 
    p += sprintf(outString, "NoLow");
  else {
    p += sprintf(outString, "%s (", StdRules_handTypeNames[htype]);
    if (StdRules_nSigCards[htype] >= 1) 
      p += sprintf(p, "%c", 
                   StdDeck_rankChars[CARD_TO_RANK(HandVal_TOP_CARD(hv))]);
    if (StdRules_nSigCards[htype] >= 2) 
      p += sprintf(p, " %c", 
                   StdDeck_rankChars[CARD_TO_RANK(HandVal_SECOND_CARD(hv))]);
    if (StdRules_nSigCards[htype] >= 3) 
      p += sprintf(p, " %c", 
                   StdDeck_rankChars[CARD_TO_RANK(HandVal_THIRD_CARD(hv))]);
    if (StdRules_nSigCards[htype] >= 4) 
      p += sprintf(p, " %c", 
                   StdDeck_rankChars[CARD_TO_RANK(HandVal_FOURTH_CARD(hv))]);
    if (StdRules_nSigCards[htype] >= 5) 
      p += sprintf(p, " %c", 
                   StdDeck_rankChars[CARD_TO_RANK(HandVal_FIFTH_CARD(hv))]);
    p += sprintf(p, ")");
  };

  return p - outString;
}

int 
LowHandVal_print(LowHandVal handval) {
  char buf[80];
  int n;

  n = LowHandVal_toString(handval, buf);
  printf("%s", buf);
  return n;
}
