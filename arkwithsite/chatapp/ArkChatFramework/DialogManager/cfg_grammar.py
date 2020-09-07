# -*- encoding: utf-8 -*-

#
# cfg_grammar.py
# Copyright (C) 2009, Alexander Berman. All rights reserved.
#

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published 
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# and the GNU Lesser General Public License along with this program.  
# If not, see <http://www.gnu.org/licenses/>.

from nltk import parse

from chatapp.ArkChatFramework.DialogManager.ibis import *


######################################################################
# CFG grammar based on NLTK
######################################################################
class CFG_Grammar(Grammar):
    """CFG parser based on NLTK."""
    
    def loadGrammar(self, grammarFilename):
        self.parser = parse.load_parser(grammarFilename, trace=1, cache=False)

    def interpret(self, user_input):
        """Parse an user_input string into a dialogue move or a set of moves."""
        try: return self.parseString(user_input)
        except: pass
        try: return eval(user_input)
        except: pass
        return set([])

    def parseString(self, user_input):
        tokens = user_input.split()
        try:
            #nbest_parse was deprecated in NLTK 3.0,
#             trees = self.parser.nbest_parse(tokens)
#             trees = self.parser.parse(tokens)
            trees = next(self.parser.parse(tokens))
#             sem = trees[0].node['sem'].simplify()
            sem = trees[0].label().get('sem')
            print("trees[0].label()=++{}++".format(sem))
        except Exception as ex: # 파싱오류 처리
            print('parsing error : ', ex)
        return self.sem2move(sem)

    def sem2move(self, sem):
        try: 
            return Answer(sem['Answer'])
#         except Exception as ex: # ?��?�� 종류
#             print('?��?���? 발생 ?��?��?��?��', ex)
        except: pass
        try:
#             print("sem2move(self, sem) --> Answer(pred+'(+ind+)')")
            ans = sem['Answer']
            pred = ans['pred']
            ind = ans['ind']
            #return Answer(Prop((Pred1(pred, Ind(ind), True))))
            return Answer(pred+"("+ind+")")
        except: pass
        try: 
#             print("sem2move(self, sem) --> Ask(WhQ(Pred1(sem['Ask'])))")
            return Ask(WhQ(Pred1(sem['Ask'])))
        except: pass
        print("sem2move(self, sem) --> None")
        return None

