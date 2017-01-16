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
#include "deck_astud.h"
#include "rules_astud.h"

const char *AStudRules_handTypeNames[AStudRules_HandType_LAST+1] = {
  "NoPair",
  "OnePair",
  "TwoPair",
  "Trips",
  "Straight",
  "FlHouse",
  "Flush",
  "Quads",
  "StFlush"
};

const char *AStudRules_handTypeNamesPadded[AStudRules_HandType_LAST+1] = {
  "NoPair  ",
  "OnePair ",
  "TwoPair ",
  "Trips   ",
  "Straight",
  "FlHouse ",
  "Flush   ",
  "Quads   ",
  "StFlush "
};

int AStudRules_nSigCards[AStudRules_HandType_LAST+1] = {
  5, 
  4, 
  3, 
  3, 
  1, 
  2,
  5, 
  2, 
  1
};


int 
AStudRules_HandVal_toString(HandVal handval, char *outString) {
  char *p = outString;
  int htype = HandVal_HANDTYPE(handval);

  p += sprintf(outString, "%s (", AStudRules_handTypeNames[htype]);
  if (AStudRules_nSigCards[htype] >= 1) 
    p += sprintf(p, "%c", 
                 AStudDeck_rankChars[HandVal_TOP_CARD(handval)]);
  if (AStudRules_nSigCards[htype] >= 2) 
    p += sprintf(p, " %c", 
                 AStudDeck_rankChars[HandVal_SECOND_CARD(handval)]);
  if (AStudRules_nSigCards[htype] >= 3) 
    p += sprintf(p, " %c", 
                 AStudDeck_rankChars[HandVal_THIRD_CARD(handval)]);
  if (AStudRules_nSigCards[htype] >= 4) 
    p += sprintf(p, " %c", 
                 AStudDeck_rankChars[HandVal_FOURTH_CARD(handval)]);
  if (AStudRules_nSigCards[htype] >= 5) 
    p += sprintf(p, " %c", 
                 AStudDeck_rankChars[HandVal_FIFTH_CARD(handval)]);
  p += sprintf(p, ")");

  return p - outString;
}

int 
AStudRules_HandVal_print(HandVal handval) {
  char buf[80];
  int n;

  n = AStudRules_HandVal_toString(handval, buf);
  printf("%s", buf);
  return n;
}

