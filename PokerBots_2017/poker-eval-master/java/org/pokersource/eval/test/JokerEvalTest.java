// $Id: JokerEvalTest.java 384 2004-05-11 06:27:47Z mjmaurer $

package org.pokersource.eval.test;

import junit.framework.TestCase;
import org.pokersource.eval.JokerEval;
import org.pokersource.game.Deck;

/**
 @author Michael Maurer &lt;<a href="mailto:mjmaurer@yahoo.com">mjmaurer@yahoo.com</a>&gt;
 */

public class JokerEvalTest extends TestCase {
  private int[] ranks;
  private int[] suits;

  public JokerEvalTest(String name) {
    super(name);
  }

  public static void main(String args[]) {
    junit.textui.TestRunner.run(JokerEvalTest.class);
  }

  protected void setUp() {
    ranks = new int[5];
    suits = new int[5];
    ranks[0] = Deck.RANK_3;
    suits[0] = Deck.SUIT_HEARTS;
    ranks[1] = Deck.RANK_4;
    suits[1] = Deck.SUIT_HEARTS;
    ranks[2] = Deck.RANK_5;
    suits[2] = Deck.SUIT_HEARTS;
    ranks[3] = Deck.RANK_JOKER;
    suits[3] = Deck.SUIT_JOKER;
    ranks[4] = Deck.RANK_7;
    suits[4] = Deck.SUIT_HEARTS;
  }

  public void testEvalHigh() {
    long hival = JokerEval.EvalHigh(ranks, suits);
    assertEquals(134545408, hival);
  }

  public void testEvalLow() {
    long loval = JokerEval.EvalLow(ranks, suits);
    assertEquals(410400, loval);
  }

  public void testEvalLow8() {
    long lo8val = JokerEval.EvalLow8(ranks, suits);
    assertEquals(410400, lo8val);
  }
}
