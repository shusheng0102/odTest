**一、项目概述**

- 该项目仓库（[facebookresearch/generative - recommenders](https://github.com/facebookresearch/generative-recommenders)）用于存放“Actions Speak Louder than Words: Trillion - Parameter Sequential Transducers for Generative Recommendations”（[https://arxiv.org/abs/2402.17152, ICML'24](https://arxiv.org/abs/2402.17152, ICML'24)）论文中结果复现的相关代码。

**二、许可证**

- 代码库遵循 Apache - 2.0 许可证，详见 LICENSE 文件。

**三、贡献者**

- 项目由众多技术贡献者共同完成，具体名单（按字母顺序排列）见文档。

**四、代码结构**

- **main**：
  - **configs**：移除了已弃用的`item_feature_embedding_dim`。
  - **data**：对代码库进行了格式化。
  - **indexing**：对代码库进行了格式化。
  - **modeling**：对代码库进行了格式化。
  - **ops/triton**：添加了对`max_attn_len`的 Triton 支持。
  - **tests**：为参差不齐的注意力添加了一个单元测试。
  - **trainer**：初始提交。
- 其他文件：
  - **.gitignore**：初始提交。
  - **CODE_OF_CONDUCT.md**：初始提交。
  - **CONTRIBUTING.md**：初始提交。
  - **LICENSE**：初始提交。
  - **README.md**：更新 README.md（[May 2, 2024](May 2, 2024)）。
  - **preprocess_public_data.py**：初始提交。
  - **requirements.txt**：根据自动检查清理了 requirements.txt（[Jun 22, 2024](Jun 22, 2024)）。
  - **train.py**：对代码库进行了格式化（[Jun 27, 2024](Jun 27, 2024)）。

**五、开始步骤**

- **安装依赖**：根据官方说明安装 PyTorch，然后执行`pip3 install gin - config absl - py scikit - learn scipy matplotlib numpy apex hypothesis pandas fbgemm_gpu iopath`。
- **下载和预处理数据**：执行`mkdir - p tmp/ && python3 preprocess_public_data.py`。
- **运行模型训练**：对于大多数数据集，具有 24GB 或更多 HBM 的 GPU 应该可行。例如，执行`CUDA_VISIBLE_DEVICES=0 python3 train.py --gin_config_file=configs/ml - 1m/hstu - sampled - softmax - n128 - large - final.gin --master_port=12345`。其他配置包含在`configs/ml - 1m`、`configs/ml - 20m`和`configs/amzn - books`中，以便更轻松地复现这些实验。
- **验证结果**：默认将实验日志写入`exps/`。可以使用类似`tensorboard --logdir ~/generative - recommenders/exps/ml - 1m - l200/ --port 24001 --bind_all`的命令启动 tensorboard。

**六、实验结果**

- **MovieLens - 1M (ML - 1M)**：
  - **SASRec**：`HR@10`为 0.2853，`NDCG@10`为 0.1603，`HR@50`为 0.5474，`NDCG@50`为 0.2185，`HR@200`为 0.7528，`NDCG@200`为 0.2498。
  - **BERT4Rec**：与 SASRec 相比，`HR@10`下降 0.4%，`NDCG@10`下降 4.1%。
  - **GRU4Rec**：与 SASRec 相比，`HR@10`下降 1.5%，`NDCG@10`上升 2.8%。
  - **HSTU**：与 SASRec 相比，`HR@10`上升 8.6%，`NDCG@10`上升 7.3%，`HR@50`上升 5.1%，`NDCG@50`上升 5.6%，`HR@200`上升 2.5%，`NDCG@200`上升 4.3%。
  - **HSTU - large**：与 SASRec 相比，`HR@10`上升 15.5%，`NDCG@10`上升 18.1%，`HR@50`上升 8.4%，`NDCG@50`上升 13.5%，`HR@200`上升 4.1%，`NDCG@200`上升 10.9%。
- **MovieLens - 20M (ML - 20M)**：
  - **SASRec**：`HR@10`为 0.2889，`NDCG@10`为 0.1621，`HR@50`为 0.5503，`NDCG@50`为 0.2199，`HR@200`为 0.7661，`NDCG@200`为 0.2527。
  - **BERT4Rec**：与 SASRec 相比，`HR@10`下降 2.5%，`NDCG@10`上升 5.1%。
  - **GRU4Rec**：与 SASRec 相比，`HR@10`下降 2.6%，`NDCG@10`上升 6.7%。
  - **HSTU**：与 SASRec 相比，`HR@10`上升 13.3%，`NDCG@10`上升 16.9%，`HR@50`上升 7.0%，`NDCG@50`上升 12.5%，`HR@200`上升 3.8%，`NDCG@200`上升 10.3%。
  - **HSTU - large**：与 SASRec 相比，`HR@10`上升 23.1%，`NDCG@10`上升 29.4%，`HR@50`上升 11.6%，`NDCG@50`上升 21.5%，`HR@200`上升 5.4%，`NDCG@200`上升 17.4%。
- **Amazon Reviews (Books)**：
  - **SASRec**：`HR@10`为 0.0306，`NDCG@10`为 0.0164，`HR@50`为 0.0754，`NDCG@50`为 0.0260，`HR@200`为 0.1431，`NDCG@200`为 0.0362。
  - **HSTU**：与 SASRec 相比，`HR@10`上升 36.4%，`NDCG@10`上升 39.3%，`HR@50`上升 27.1%，`NDCG@50`上升 32.3%，`HR@200`上升 21.3%，`NDCG@200`上升 27.7%。
  - **HSTU - large**：与 SASRec 相比，`HR@10`上升 56.7%，`NDCG@10`上升 60.7%，`HR@50`上升 43.7%，`NDCG@50`上升 51.2%，`HR@200`上升 33.4%，`NDCG@200`上升 43.2%。

以上三个表格中，SASRec 行基于 Self - Attentive Sequential Recommendation，但将原始的二进制交叉熵损失替换为 Revisiting Neural Retrieval on Accelerators 中提出的采样 softmax 损失。这些行可以使用`configs/*/sasrec - * - final.gin`进行复现。BERT4Rec 和 GRU4Rec 行基于 Turning Dross Into Gold Loss: is BERT






关于GitHub上的`facebookresearch/generative-recommenders`项目，以下是一些关键信息：

### 项目概述

* **项目名称**：Generative Recommenders
* **GitHub仓库**：[facebookresearch/generative-recommenders](https://github.com/facebookresearch/generative-recommenders)
* **目的**：该项目基于即将在ICML'24上发表的论文《Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations》，旨在通过万亿参数级别的序列转换器革新推荐算法的边界。

### 项目特点

1. **开源代码库**：Generative Recommenders是一个开源项目，提供了复现实验所需的代码，尤其是对传统顺序推荐场景下的验证（如MovieLens和Amazon Reviews数据集）。
2. **创新架构**：项目核心在于其创新的HSTU（Hierarchical Sequence Transformer Unit）架构，设计用于处理大规模的推荐任务，能够有效学习用户的动态行为模式。
3. **高精度与可扩展性**：HSTU模型在多个基准数据集上的测试结果显示，相比标准模型（如SASRec、BERT4Rec）在HR@N和NDCG@N指标上有显著提升。同时，支持万亿级参数，为处理大规模数据集铺平道路。
4. **高效计算**：尽管依赖高性能GPU（至少24GB HBM内存），但项目规划未来发布自定义内核以优化性能。
5. **全面文档**：随着项目进展，将有更多技术报告和说明文档，便于理解和应用。

### 应用场景

Generative Recommenders特别适用于那些需要高度精准且个性化的推荐场景，如视频流媒体服务、电商产品推荐、在线阅读平台等。通过该项目，开发者可以构建更为智能的推荐引擎，不仅能预测用户可能感兴趣的内容，还能生成高质量的潜在兴趣推荐列表，从而提升用户体验，增加用户粘性。

### 如何参与

* **访问GitHub仓库**：直接访问[facebookresearch/generative-recommenders](https://github.com/facebookresearch/generative-recommenders)以获取最新代码和文档。
* **阅读文档**：阅读项目提供的文档和示例，了解如何使用HSTU架构进行推荐系统开发。
* **贡献代码**：如果您对项目有改进意见或新的功能实现，可以通过GitHub的Pull Request流程提交您的代码。

总之，Generative Recommenders是一个前沿的推荐系统项目，通过创新的HSTU架构和万亿参数级别的模型规模，为推荐算法的发展开辟了新的方向。对于致力于提升用户体验、探索推荐系统极限的技术团队来说，这无疑是一个值得一试的宝藏项目。




Generative Recommenders项目的工作方式主要基于其创新的HSTU（Hierarchical Sequence Transformer Unit）架构，这是一个用于处理大规模推荐任务的深度学习模型。以下是对该项目工作方式的详细解释：

### 1. 架构与设计

* **HSTU架构**：HSTU是该项目的核心，它设计用于处理高基数和动态的推荐数据流。与传统的Transformer结构相比，HSTU通过去除Softmax函数并采用按位点乘的方式，直接处理稀疏特征，从而优化了模型对稀疏数据的处理能力。这种设计显著提高了计算效率，特别是在长序列处理上。
* **特征统一**：项目对DLRMs（深度学习推荐模型）中的异构特征空间进行了序列化和统一处理。随着序列长度趋于无限大，新方法逼近完整的DLRM特征空间，使得模型能够更有效地捕捉推荐系统中的复杂交互关系。

### 2. 工作流程

* **数据输入**：系统接收用户的历史行为数据（如点击、浏览、购买记录等）作为输入。这些数据被编码为一系列的特征向量。
* **特征处理**：HSTU模型对输入的特征向量进行处理，通过其独特的自注意力机制和按位点乘操作，捕捉用户行为的动态模式和特征间的复杂交互关系。
* **序列转导**：在生成式推荐框架下，模型将推荐系统的主要任务（排名和检索）转化为序列转导任务。即，模型学习如何从用户的历史行为序列中预测出下一个可能感兴趣的项目。
* **输出与推荐**：模型输出每个候选项目的预测概率或评分，根据这些预测结果生成推荐列表。推荐列表中的项目按照预测概率或评分的降序排列，以展示给用户。

### 3. 性能与优势

* **高精度**：HSTU模型在多个基准数据集上的测试结果显示，相比标准模型（如SASRec、BERT4Rec）在HR@N和NDCG@N指标上有显著提升。
* **可扩展性**：支持万亿级参数，为处理大规模数据集铺平道路。这使得模型能够应对日益增长的用户和数据量，保持推荐系统的性能和准确性。
* **高效计算**：尽管依赖高性能GPU（至少24GB HBM内存），但项目规划未来发布自定义内核以优化性能。这将进一步提高模型的计算效率，降低运行成本。

### 4. 应用场景

Generative Recommenders特别适用于那些需要高度精准且个性化的推荐场景，如视频流媒体服务、电商产品推荐、在线阅读平台等。通过该项目，开发者可以构建更为智能的推荐引擎，不仅能预测用户可能感兴趣的内容，还能生成高质量的潜在兴趣推荐列表，从而提升用户体验，增加用户粘性。

### 5. 未来发展

随着项目的不断推进和研究的深入，Generative Recommenders有望在未来实现更多的创新和发展。例如，通过引入更多的特征表示方法和优化算法，进一步提高模型的性能和准确性；通过与其他技术的结合（如自然语言处理、计算机视觉等），实现多模态的推荐系统；以及通过在实际应用场景中的部署和测试，不断优化和完善模型。

总之，Generative Recommenders项目通过其创新的HSTU架构和生成式推荐框架，为推荐系统的发展提供了新的思路和方法。随着技术的不断进步和应用场景的不断拓展，该项目有望在未来发挥更大的作用和价值。



推荐项目：Generative Recommenders——打造下一代推荐系统
在数据驱动的时代，个性化推荐已成为连接用户与信息的桥梁。今天，我们要向您隆重推荐一个前沿项目——Generative Recommenders。该项目基于即将在ICML'24上发表的论文《Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations》，旨在通过万亿参数级别的序列转换器革新推荐算法的边界。

项目简介
Generative Recommenders是一个开源代码库，专注于实现“行动胜于言语”的理念，利用深度学习的力量，特别是高效率的序列模型HSTU（Hierarchical Sequence Transformer Unit），来提升推荐系统的性能。该库目前提供了复现实验所需的代码，尤其是对传统顺序推荐场景下的验证（如MovieLens和Amazon Reviews数据集），让我们能直接感受到HSTU相较于其他方法（如SASRec、BERT4Rec和GRU4Rec）的优势。

技术分析
本项目的核心在于其创新的HSTU架构，设计用于处理大规模的推荐任务，它能够有效学习用户的动态行为模式，并通过 trillion-parameter 级别的模型规模突破推荐精度和召回率的限制。在实践中，HSTU通过引入更高效的采样softmax损失函数，优化了原有的自我注意力机制，显著提高了模型在处理海量数据时的表现力。

应用场景
Generative Recommenders特别适用于那些需要高度精准且个性化的推荐场景，如视频流媒体服务、电商产品推荐、在线阅读平台等。通过该项目，开发者可以构建更为智能的推荐引擎，不仅能预测用户可能感兴趣的内容，还能生成高质量的潜在兴趣推荐列表，从而提升用户体验，增加用户粘性。特别是在电影、图书和商品推荐领域，HSTU及其大模型版本(HSTU-large)已经展示了超越现有方法的明显优势。

项目特点
高精度表现：HSTU模型在多个基准数据集上的测试结果显示，相比标准模型如SASRec、BERT4Rec，在HR@N和NDCG@N指标上有显著提升。
可扩展性：支持万亿级参数，为处理大规模数据集铺平道路。
易复现研究：提供详细实验步骤和配置文件，使研究人员可以轻松复现结果并进行进一步探索。
高效计算设计：尽管依赖高性能GPU（至少24GB HBM内存），但项目规划未来发布自定义内核以优化性能。
全面文档：随着项目进展，将有更多技术报告和说明文档，便于理解和应用。
结语
对于致力于提升用户体验、探索推荐系统极限的技术团队来说，Generative Recommenders无疑是值得一试的宝藏项目。它不仅代表了当前推荐系统技术的尖端水平，也为未来的推荐算法发展开辟了新的方向。加入这个社区，一起探索如何用AI的力量让每一次推荐都更加精准、贴心！

————————————————

                        版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。
原文链接：https://blog.csdn.net/gitblog_00059/article/details/139670082





作者：萧瑟
链接：https://www.zhihu.com/question/646766849/answer/3428951063
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

论文工作还挺有意思的。之前有AutoInt等用[transformer](https://www.zhihu.com/search?q=transformer&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)做特征自动交叉的工作，也有[Transformers4Rec](https://www.zhihu.com/search?q=Transformers4Rec&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)等把transformer用到[序列建模](https://www.zhihu.com/search?q=%E5%BA%8F%E5%88%97%E5%BB%BA%E6%A8%A1&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)的工作，这个工作把用户画像和用户行为甚至target信息都放到超长序列中，结合多层（应该是精排3层，召回6层，最多24层）transformer进行建模，很简洁。看文章有可能是[meta](https://www.zhihu.com/search?q=meta&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)的短视频推荐业务，由于不知道线上[baseline](https://www.zhihu.com/search?q=baseline&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)的具体情况，因此推测效果来源可能有下面几点：

1. 更强的[特征交叉](https://www.zhihu.com/search?q=%E7%89%B9%E5%BE%81%E4%BA%A4%E5%8F%89&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)能力：直接在原始用户行为上引入用户画像和target信息进行交叉，没有信息损失，交叉更为充分。而很多特征交叉工作是在用户建模处理后已经压缩的用户表征上进行，信息损失比较大。当然也有[笛卡尔积](https://www.zhihu.com/search?q=%E7%AC%9B%E5%8D%A1%E5%B0%94%E7%A7%AF&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)和CAN等工作是在原始用户行为上进行，不过建模能力有可能弱于多层transformer结构。另外看论文工作embedding维度可能是512这个维度，因此模型容量应该也是足够的。另外不知道baseline有没有类似senet、[ppnet](https://www.zhihu.com/search?q=ppnet&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)这种gateing网络，如果没有的话，新架构应该也会有更多效果增强。
2. 信息利用更充分：对稀疏参数来说，自回归预测next item的loss，相比原来样本维度的[交叉熵](https://www.zhihu.com/search?q=%E4%BA%A4%E5%8F%89%E7%86%B5&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)loss，参数的梯度更新可能会更充分，样本利用效率也会更高。这个感觉非常像DIEN中的[辅助loss](https://www.zhihu.com/search?q=%E8%BE%85%E5%8A%A9loss&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)。
3. 更丰富的用户行为引入以及更强的序列建模能力：根据作者知乎回答来看，baseline包含多条序列建模模块，并且新模型使用的用户序列长度甚至比baseline还短，且新模型使用特征是baseline的子集，那么效果可能主要来自于更强的[用户行为建模](https://www.zhihu.com/search?q=%E7%94%A8%E6%88%B7%E8%A1%8C%E4%B8%BA%E5%BB%BA%E6%A8%A1&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)能力。当然新架构也有能力使用更丰富的用户行为信号（例如baseline只使用点击，新架构引入了曝光等）。

![](https://picx.zhimg.com/80/v2-bc39959d34b9299718cd785fec53629c_720w.webp?source=2c26e567)

论文中[cross attention](https://www.zhihu.com/search?q=cross%20attention&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)的实现，感觉挺有意思的。如果在[CTR](https://www.zhihu.com/search?q=CTR&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)推荐场景落地论文的架构，有可能是把曝光和点击行为，都放到一条序列中，把item的[time diff](https://www.zhihu.com/search?q=time%20diff&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)、类目等属性信息以类似[position embedding](https://www.zhihu.com/search?q=position%20embedding&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)的方式相加引入进来，把行为类型也放到了序列中，序列形式类似于：item1，action（曝光未点击），item2，action（点击），item3，action（点击）。。。后面是一个next item prediction的loss，[精排模型](https://www.zhihu.com/search?q=%E7%B2%BE%E6%8E%92%E6%A8%A1%E5%9E%8B&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)会mask掉序列中的用户画像和action部分，而在item位置后接一个小网络进行多任务action目标的预测。召回模型则只对序列中的item进行预测，不过会把像曝光未点击这类item mask掉。

论文中出现的scaling law现象令人振奋，不过LLM的scaling law论文中提到，参数量和数据集大小要同步增加，只提升一个的话会有效果提升幅度的惩罚，不知道论文中进行实验的时候，数据集大小是怎么变化的，是否有足够的数据来支撑。另外LLM的scaling law论文中在讨论计算量参数量的时候，是把embedding层排除掉了，这个论文中应该没有排除，不知道是不是推荐和NLP大模型scaling law上的一个差异点。

论文虽然抛弃了人工构造的统计特征，但仍然是基于[ID体系](https://www.zhihu.com/search?q=ID%E4%BD%93%E7%B3%BB&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)进行学习的，并没有多模态信息的引入。目前一些研究表明，多模态信息在一些情况下是可以打平ID体系的，不知道后面结合模型复杂度和数据量的提升，是否会有一些质的飞跃，这个还是比较期待的。

[线上推理](https://www.zhihu.com/search?q=%E7%BA%BF%E4%B8%8A%E6%8E%A8%E7%90%86&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)阶段，可以把上百个精排候选集放到序列中，一次推理即可得到所有打分结果，而且随着候选集数目的上升，相比传统架构的优势也越来越明显。推测应该是[decode-only架构](https://www.zhihu.com/search?q=decode-only%E6%9E%B6%E6%9E%84&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)，用了causal mask的方式，序列中每个item在做attention的时候，只能看到自己和之前的item，看不到后面的item。模型能力比历史行为和target item拼一起直接做 self attention要低，比历史行为做完self attention之后再做[target attention](https://www.zhihu.com/search?q=target%20attention&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)要高。复杂度确实可以控制到 O((n+bm)2d)  **O((n + b_m )^2 d)** 的水平。

另外因为少了很多特征加工，[特征抽取](https://www.zhihu.com/search?q=%E7%89%B9%E5%BE%81%E6%8A%BD%E5%8F%96&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)加工部分的计算会比较简单，应该也能节省挺多机器。文章提到推理的算力成本和基线差不多，[Meta](https://www.zhihu.com/search?q=Meta&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A3428951063%7D)的工程优化能力确实很强。

后面如果尝试在自己业务复现的话，我觉得挑战可能有下面几点：

* 效果空间：取决于当前基线的特征交叉和用户建模技术水位，基线太强会影响提升的效果，那么落地这个工作可能就会不太划算。
* 工程优化：离线训练和在线推理都有挺多需要优化的地方，否则很难控制计算成本和迭代效率。
* 信息对齐：基线可能特征很多，数据来源也很多，需要尽量把基线特征用的上游数据源都梳理清楚，保证两套系统在输入信息量上是可比的。另外新架构很难把基线模型的交叉特征和统计特征加进来，给打平效果也带来了不小的困难。

Update：

代码已经开源出来了，说明作者对自己的工作质量还是比较自信的：[https://**github.com/facebookrese**arch/generative-recommenders](https://link.zhihu.com/?target=https%3A//github.com/facebookresearch/generative-recommenders)

我们跑了一下，有些数据集的实验结果比论文中还高

https://arxiv.org/abs/2402.17152v2


大规模推荐系统的特点在于它们依赖于高基数、异构特征，并且需要每天处理数千亿用户行为。尽管使用具有数千个特征的庞大数据量进行训练，但大多数工业界的深度学习推荐模型（DLRM）在计算上难以扩展。

受到Transformer在语言和视觉领域取得成功的启发，我们重新审视了推荐系统中的基本设计选择。我们将推荐问题重新构想为生成模型框架中的序列转换任务（"生成式推荐器"），并提出了一种新的架构HSTU，专为高基数、非静态的流推荐数据设计。

HSTU在合成和公共数据集上的基准测试中性能提高了高达65.8%的NDCG，并且在8192长度序列上比基于FlashAttention2的Transformer快5.3倍至15.2倍。基于HSTU的生成式推荐器，拥有1.5万亿参数，在在线A/B测试中的指标提高了12.4%，并且已经被部署在拥有数十亿用户的大型互联网平台的多个界面上。更重要的是，生成式推荐器的模型质量在三个数量级的计算训练中经验性地呈现出与训练计算的幂律关系，达到GPT-3/LLaMa-2的规模，这减少了未来模型开发所需的碳足迹，并为推荐领域的首个基础模型铺平了道路。



作为本文共同作者其中一位尝试回答一下。

首先本文亮点还是比较多的，包括且不限于

* “统一的生成式推荐”(GR) 第一次在核心产品线替换掉了近十年推荐工业界长期使用的分层海量特征的模型范式；
* 新的encoder (HSTU) 通过新架构 + 算法稀疏性加速达到了模型质量超过Transformer + 实际训练侧效率比FlashAttention2 （目前最快的Transformer实现）快15.2倍；
* 我们通过新的推理算法M-FALCON达成了推理侧700倍加速（285倍复杂模型，2.48x推理QPS）；
* 通过新架构HSTU+训练算法GR，我们模型总计算量达到了1000x级的提升，第一次达到GPT-3 175b/LLaMa-2 70b等LLM训练算力，且第一次我们在推荐模态观测到了语言模态的scaling law；
* 传统测试集MovieLens Amazon Reviews等相对经典SASRec提升20.3%-65.8% NDCG@10；
* 实际中多产品界面上线单特定ranking界面提升12.4%；
* etc.

然后回答一下题主问题：

* 12%是在线E-Task (Table 6)。"we report the main engagement event (“E-Task”) and the main consumption event (“C-Task”)." E-Task是我们最主要的在线参与度指标，可以想象成点赞转发。C-Task可以想象成完播，时长这样的任务。再另外12.4% 只是单纯ranking stage的结果，如果我们把召回+排序两个阶段加起来就12.4% (table 6) + 6.2% (table 5) = 18.6%了。。
* 自回归训练时因为核心推荐场景词表在billion级以上，采样是必须的。我们这里也有一些算法改进，限于篇幅这篇文章没有写。后续tech report或者follow up paper可能会更新。
* ranking的setup可以看2.2最后一段。“We address this problem by interleaving items and actions in the main time series. The resulting new time series (before categorical features) is then x0, a0, x1, a1, . . . , xn−1, an−1, where mask m_i's are 0s for the action positions”。我们是通过交错放置item content和item action序列来达到target aware cross attention in autoregressive setting的。后续appendix会补一下图。


文件是一篇关于生成式推荐系统（Generative Recommenders，简称GRs）的研究论文，主要内容包括：

1. **背景与动机**：大规模推荐系统需要处理高基数、异构特征，并且每天需要处理数十亿用户行为。尽管深度学习推荐模型（Deep Learning Recommendation Models，简称DLRMs）在大量数据上训练，但它们在计算上难以扩展。
2. **生成式推荐系统（GRs）**：作者提出将推荐问题重新构想为序列转换任务，并在生成模型框架内解决，称为"生成式推荐器"。特别地，提出了一种新的架构HSTU（Hierarchical Sequential Transduction Units），专为高基数、非静态的流推荐数据设计。
3. **HSTU架构**：HSTU修改了注意力机制以适应大型、非静态词汇表，并利用推荐数据集的特点，在8192长度序列上比基于FlashAttention2的Transformer快5.3倍至15.2倍。
4. **性能提升**：HSTU在合成数据集和公共数据集上的表现超过了基线模型，NDCG（一种推荐系统性能评估指标）提高了高达65.8%。在在线A/B测试中，基于HSTU的生成式推荐器提升了12.4%的指标，并且已经在拥有数十亿用户的互联网平台上部署。
5. **模型质量与计算量的关系**：生成式推荐器的模型质量在三个数量级的计算训练中显示出与训练计算量的幂律关系，这减少了未来模型开发所需的碳足迹，并为推荐领域的基础模型铺平了道路。
6. **实验**：论文中描述了在不同数据集上对HSTU进行评估的实验，包括传统的序列推荐设置和工业规模的流式设置。实验结果表明，HSTU在多种指标上优于现有的Transformer模型和其他基线模型。
7. **结论**：作者认为生成式推荐系统（GRs）提供了一种新的范式，可以更有效地处理推荐任务，并且具有更好的扩展性。通过HSTU架构和M-FALCON算法，GRs能够在保持较低推理预算的同时，显著提高模型复杂度和性能。
8. **社会影响**：论文还讨论了这项工作可能带来的积极社会影响，包括提高推荐系统的隐私友好性、改善用户体验，以及通过基础模型和规模法则减少模型研究和开发所需的碳足迹。

论文由Jiaqi Zhai、Lucy Liao、Xing Liu、Yueming Wang、Rui Li等作者撰写，并在41st International Conference on Machine Learning上发表。论文的代码可在GitHub上找到，链接为：https://github.com/facebookresearch/generative-recommenders。



由于文档内容较长，超出了单次回复的能力范围，我将提供文档的概要翻译和关键点总结。

### 文档概要翻译：

**标题**:
行动胜于雄辩：用于生成式推荐的万亿参数序列转换器

**摘要**:
大规模推荐系统以高基数、异构特征为特点，并需要每天处理数千亿用户行为。尽管深度学习推荐模型（DLRMs）在具有数千特征的庞大数据量上训练，但它们在计算上难以扩展。受Transformer在语言和视觉领域的成功启发，我们重新考虑推荐系统中的基本设计选择。我们将推荐问题重新构想为生成模型框架内的序列转换任务（“生成式推荐器”），并提出了一种新的架构HSTU，专为高基数、非静态的流推荐数据设计。HSTU在合成和公共数据集上的性能比基线模型高出65.8%，在8192长度序列上比基于FlashAttention2的Transformer快5.3到15.2倍。HSTU的生成式推荐器，拥有1.5万亿参数，在在线A/B测试中的指标提高了12.4%，并且已经在拥有数十亿用户的互联网平台上部署。更重要的是，生成式推荐器的模型质量在三个数量级的计算训练中经验性地呈现出与训练计算的幂律关系，这减少了未来模型开发所需的碳足迹，并为推荐领域的首个基础模型铺平了道路。

**1. 引言**:
推荐系统在在线内容平台和电子商务中至关重要，每天都在个性化数十亿用户体验。DLRMs在过去十年中一直是推荐领域的最先进方法。DLRMs以使用异构特征为特点，例如数值特征、嵌入和分类特征等。尽管利用了大量人工设计的特征集和大量数据训练，但大多数工业界的DLRMs在计算上扩展性差。

**2. 推荐作为序列转换任务：从DLRMs到GRs**:
我们将DLRMs中的异构特征空间统一起来，并将排名和检索任务重新构想为序列转换任务。

**3. 生成式推荐器的性能**:
我们提出了一种新的序列转换架构HSTU，它通过修改注意力机制来处理大型、非静态词汇表，并利用推荐数据集的特点来提高速度。

**4. 实验**:
我们在合成数据集、公共数据集以及在大型互联网平台的多个界面上进行了实验，验证了所提出技术的有效性。

**5. 相关工作**:
讨论了先前关于序列推荐器的研究，以及在推荐系统中应用Transformer的相关工作。

**6. 结论**:
我们提出了一种新的推荐系统范式，通过HSTU编码器设计和M-FALCON算法，GRs在生产环境中的性能比DLRMs提高了12.4%。

**影响声明**:
我们的工作对推荐、搜索和广告系统有广泛的积极影响，包括提高隐私友好性、改善用户体验，并减少模型研究和开发所需的碳足迹。

### 关键点总结：

- **主题**: 提出了一种新的生成式推荐系统架构HSTU，用于处理大规模推荐任务。
- **性能**: HSTU在多个数据集上表现优异，比现有模型快5.3到15.2倍。
- **规模**: HSTU能够处理高达1.5万亿参数的模型。
- **部署**: 在数十亿用户的大型互联网平台上部署，并提高了在线A/B测试的指标。
- **环境影响**: 减少了未来模型开发所需的碳足迹。
- **社会影响**: 提高了推荐系统的隐私友好性和用户体验。

请注意，这是对文档内容的高度概括和翻译，具体细节和实验结果需要深入阅读原文来获取。
